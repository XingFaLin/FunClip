    # gradio interface
    theme = gr.Theme.load("funclip/utils/theme.json")
    with gr.Blocks(theme=theme) as funclip_service:
        with gr.Row():
            with gr.Column():
                with gr.Tab("🎥 视频/音频识别 | Video/Audio Recognition"):
                    video_input = gr.Video(label="📹 视频文件 | Video File")
                    audio_input = gr.Audio(label="🎧 音频文件 | Audio File")
                    hotwords_input = gr.Textbox(label="🔥 热词 | Hotwords (多个热词用逗号分隔)")
                    output_dir = gr.Textbox(label="📂 输出目录 | Output Directory (可选)")
                    with gr.Row():
                        recog_button = gr.Button("🎙️ 识别 | Recognize", variant="primary")
                        recog_button2 = gr.Button("🎙️ 识别+说话人 | Recognize+Speaker")
                    video_text_output = gr.Textbox(label="📝 识别文本 | Recognized Text")
                    video_srt_output = gr.Textbox(label="📖 识别SRT字幕 | Recognized SRT Subtitles")
                with gr.Tab("🧠 LLM智能裁剪 | LLM AI Clipping"):
                    with gr.Row():
                        prompt_head = gr.Textbox(label="Prompt System（不需要修改，会自动拼接左下角的srt字幕）", value=("这是待裁剪的视频srt字幕："))
                    with gr.Column():
                        with gr.Row():
                            llm_model = gr.Dropdown(
                                choices=["qwen-plus", "gpt-3.5-turbo", "gpt-3.5-turbo-0125", "gpt-4-turbo", "g4f-gpt-3.5-turbo", "moonshot-v1-8K"],
                                value="qwen-plus",
                                label="LLM Model Name"
                            )
                            apikey_input = gr.Textbox(label="APIKEY")
                            api_base_input = gr.Textbox(label="API地址(可选)", placeholder="https://api.openai.com/v1")
                            clip_count = gr.Number(label="生成片段数量 | Clip Count", value=1, precision=0, minimum=1)
                            clip_second = gr.Number(label="每个片段时长 | Clip Second", value=180, precision=0, minimum=1)
                        llm_button = gr.Button("LLM推理 | LLM Inference（首先进行识别，非g4f需配置对应apikey）", variant="primary")
                    llm_result = gr.Textbox(label="LLM Clipper Result")
                    with gr.Row():
                        llm_clip_button = gr.Button("🧠 LLM智能裁剪 | AI Clip", variant="primary")
                        llm_clip_subti_button = gr.Button("🧠 LLM智能裁剪+字幕 | AI Clip+Subtitles")
                with gr.Tab("✂️ 根据文本/说话人裁剪 | Text/Speaker Clipping"):
                    video_text_input = gr.Textbox(label="✏️ 待裁剪文本 | Text to Clip (多段文本使用'#'连接)")
                    video_spk_input = gr.Textbox(label="✏️ 待裁剪说话人 | Speaker to Clip (多个说话人使用'#'连接)")
                    with gr.Row():
                        clip_button = gr.Button("✂️ 裁剪 | Clip", variant="primary")
                        clip_subti_button = gr.Button("✂️ 裁剪+字幕 | Clip+Subtitles")
                    with gr.Row():
                        video_start_ost = gr.Slider(minimum=-500, maximum=1000, value=0, step=50, label="⏪ 开始位置偏移 | Start Offset (ms)")
                        video_end_ost = gr.Slider(minimum=-500, maximum=1000, value=100, step=50, label="⏩ 结束位置偏移 | End Offset (ms)")
                with gr.Row():
                    font_size = gr.Slider(minimum=10, maximum=100, value=32, step=2, label="🔠 字幕字体大小 | Subtitle Font Size")
                    font_color = gr.Radio(["black", "white", "green", "red"], label="🌈 字幕颜色 | Subtitle Color", value='white')
            video_output = gr.Video(label="裁剪结果 | Video Clipped")
            audio_output = gr.Audio(label="裁剪结果 | Audio Clipped")
            clip_message = gr.Textbox(label="⚠️ 裁剪信息 | Clipping Log")
            srt_clipped = gr.Textbox(label="📖 裁剪部分SRT字幕内容 | Clipped RST Subtitles")
        
        recog_button.click(mix_recog, inputs=[video_input, audio_input, hotwords_input, output_dir], outputs=[video_text_output, video_srt_output, video_state, audio_state])
        recog_button2.click(mix_recog_speaker, inputs=[video_input, audio_input, hotwords_input, output_dir], outputs=[video_text_output, video_srt_output, video_state, audio_state])
        clip_button.click(mix_clip, inputs=[video_text_input, video_spk_input, video_start_ost, video_end_ost, video_state, audio_state, output_dir], outputs=[video_output, audio_output, clip_message, srt_clipped])
        clip_subti_button.click(video_clip_addsub, inputs=[video_text_input, video_spk_input, video_start_ost, video_end_ost, video_state, output_dir, font_size, font_color], outputs=[video_output, clip_message, srt_clipped])
        llm_button.click(llm_inference, inputs=[prompt_head, prompt_head2, video_srt_output, llm_model, apikey_input, api_base_input, clip_count, clip_second], outputs=[llm_result])
        llm_clip_button.click(AI_clip, inputs=[llm_result, video_text_input, video_spk_input, video_start_ost, video_end_ost, video_state, audio_state, output_dir, clip_count], outputs=[video_output, audio_output, clip_message, srt_clipped])
        llm_clip_subti_button.click(AI_clip_subti, inputs=[llm_result, video_text_input, video_spk_input, video_start_ost, video_end_ost, video_state, audio_state, output_dir], outputs=[video_output, audio_output, clip_message, srt_clipped])
    
    # start gradio service in local or share
    if args.listen:
        funclip_service.launch(share=args.share, server_port=args.port, server_name=server_name, inbrowser=False)
    else:
        funclip_service.launch(share=args.share, server_port=args.port, server_name=server_name)