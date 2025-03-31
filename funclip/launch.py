from llm.g4f_openai_api import g4f_openai_call
from utils.trans_utils import extract_timestamps
from introduction import top_md_1, top_md_3, top_md_4


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='argparse testing')
    parser.add_argument('--lang', '-l', type=str, default = "zh", help="language")
    parser.add_argument('--share', '-s', action='store_true', help="if to establish gradio share link")
    parser.add_argument('--port', '-p', type=int, default=7860, help='port number')
    parser.add_argument('--listen', action='store_true', help="if to listen to all hosts")
    args = parser.parse_args()
    
    if args.lang == 'zh':
        funasr_model = AutoModel(model="iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
                                vad_model="damo/speech_fsmn_vad_zh-cn-16k-common-pytorch",
                                punc_model="damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
                                spk_model="damo/speech_campplus_sv_zh-cn_16k-common",
                                )
    else:
        funasr_model = AutoModel(model="iic/speech_paraformer_asr-en-16k-vocab4199-pytorch",
                                vad_model="damo/speech_fsmn_vad_zh-cn-16k-common-pytorch",
                                punc_model="damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
                                spk_model="damo/speech_campplus_sv_zh-cn_16k-common",
                                )
    audio_clipper = VideoClipper(funasr_model)
    audio_clipper.lang = args.lang
    
    server_name='127.0.0.1'
    if args.listen:
        server_name = '0.0.0.0'
        
        

    def audio_recog(audio_input, sd_switch, hotwords, output_dir):
        return audio_clipper.recog(audio_input, sd_switch, None, hotwords, output_dir=output_dir)

    def video_recog(video_input, sd_switch, hotwords, output_dir):
        return audio_clipper.video_recog(video_input, sd_switch, hotwords, output_dir=output_dir)

    def video_clip(dest_text, video_spk_input, start_ost, end_ost, state, output_dir):
        return audio_clipper.video_clip(
            dest_text, start_ost, end_ost, state, dest_spk=video_spk_input, output_dir=output_dir
            )

    def mix_recog(video_input, audio_input, hotwords, output_dir):
        output_dir = output_dir.strip()
        if not len(output_dir):
            output_dir = None
        else:
            output_dir = os.path.abspath(output_dir)
        audio_state, video_state = None, None
        if video_input is not None:
            res_text, res_srt, video_state = video_recog(
                video_input, 'No', hotwords, output_dir=output_dir)
            return res_text, res_srt, video_state, None
        if audio_input is not null:
            res_text, res_srt, audio_state = audio_recog(
                audio_input, 'No', hotwords, output_dir=output_dir)
            return res_text, res_srt, None, audio_state
    
    def mix_recog_speaker(video_input, audio_input, hotwords, output_dir):
        output_dir = output_dir.strip()
        if not len(output_dir):
            output_dir = None
        else:
            output_dir = os.path.abspath(output_dir)
        audio_state, video_state = None, None
        if video_input is not None:
            res_text, res_srt, video_state = video_recog(
                video_input, 'Yes', hotwords, output_dir= output_dir)
            return res_text, res_srt, video_state, None
        if audio_input is not None:
            res_text, res_srt, audio_state = audio_recog(
                audio_input, 'Yes', hotwords, output_dir=output_dir)
            return res_text, res_srt, None, audio_state
    
    def mix_clip(dest_text, video_spk_input, start_ost, end_ost, video_state, audio_state, output_dir):
        output_dir = output_dir.strip()
        if not len(output_dir):
            output_dir = None
        else:
            output_dir = os.path.abspath(output_dir)
        if video_state is not None:
            clip_video_file, message, clip_srt = audio_clipper.video_clip(
                dest_text, start_ost, end_ost, video_state, dest_spk=video_spk_input, output_dir=output_dir)
            return clip_video_file, None, message, clip_srt
        if audio_state is not None:
            (sr, res_audio), message, clip_srt = audio_clipper.clip(
                dest_text, start_ost, end_ost, audio_state, dest_spk=video_spk_input, output_dir=output_dir)
            return None, (sr, res_audio), message, clip_srt
    
    def video_clip_addsub(dest_text, video_spk_input, start_ost, end_ost, state, output_dir, font_size, font_color):
        output_dir = output_dir.strip()
        if not len(output_dir):
            output_dir = None
        else:
            output_dir = os.path.abspath(output_dir)
        return audio_clipper.video_clip(
            dest_text, start_ost, end_ost, state, 
            font_size=font_size, font_color=font_color, 
            add_sub=True, dest_spk=video_spk_input, output_dir=output_dir
            )
    # 添加配置加载函数
    def load_llm_config():
        config_path = Path(__file__).parent.parent / "config" / "config.toml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return toml.load(f)
        return {}
        
    def llm_inference(system_content, user_content, srt_text, model, apikey, api_base, clip_count, clip_second):
        """
        SUPPORT_LLM_PREFIX = ['qwen', 'gpt', 'g4f', 'moonshot']
        if model.startswith('qwen'):
            return call_qwen_model(apikey, model, user_content+'
'+srt_text, system_content)
        if model.startswith('gpt') or model.startswith('moonshot'):
            return openai_call(apikey, model, system_content, user_content+'
'+srt_text, api_base)
        elif model.startswith('g4f'):
            model = "-".join(model.split('-')[1:])
            return g4f_openai_call(model, system_content, user_content+'
'+srt_text)
        else:
            logging.error("LLM name error, only {} are supported as LLM name prefix."
                          .format(SUPPORT_LLM_PREFIX))
        """
        llm_config = load_llm_config().get('llm', {})
        apikey = llm_config.get('api_key', '')
        api_base = llm_config.get('base_url', None)
        model = llm_config.get('model', 'qwen')
        print("apikey = ", apikey)
        print("api_base = ", api_base)
        print("model = ", model)
        llm_config = load_llm_config().get('llm', {})

         # 添加类型校验
        clip_count = int(clip_count)
        clip_second = int(clip_second)

        #将clip_count插入prompt
        phase1_prompt = """你是一个视频srt字幕分析剪辑器，输入视频的srt字幕，
                           分析其中的精彩且尽可能连续的片段并裁剪出来，可以输出{clip_count}个高质量片段组，要求，
                           将片段中在时间上连续的多个句子及它们的时间戳合并为一条，注意确保文字与时间戳的正确匹配。
                           🔥 每组必须是一个完整叙事单元（包含起因、经过、结果）
                           🔥 单组时长建议{clip_second}秒以上
                           🔥 组内句子必须语义连贯、逻辑完整
                           🔥 允许组间少量重复关键信息（<10%）
                           【输出格式】
                           组1:
                           1. [开始时间-结束时间] 文本（注意其中的连接符是“-”）
                           2. [开始时间-结束时间] 文本（注意其中的连接符是“-”）
                           ..
                           【强制要求】
                           ⚠️ 禁止拆分完整语义单元
                           ⚠️ 每组必须包含完整叙事要素
                           ⚠️ 时间戳必须连续且覆盖完整内容  
                           ⚠️ 输出格式严格按照上述格式，不要输出任何其他内容"""                                
        phase1_prompt = phase1_prompt.format(
           clip_count=clip_count,
           clip_second=clip_second
        )    
        #print("phase1_prompt = ", phase1_prompt)      

        return openai_call(apikey, model, phase1_prompt, user_content+'
'+srt_text, api_base)        
         

    """
    def AI_clip(LLM_res, dest_text, video_spk_input, start_ost, end_ost, video_state, audio_state, output_dir):
        timestamp_list = extract_timestamps(LLM_res)
        output_dir = output_dir.strip()
        if not len(output_dir):
            output_dir = None
        else:
            output_dir = os.path.abspath(output_dir)
        if video_state is not None:
            clip_video_file, message, clip_srt = audio_clipper.video_clip(
                dest_text, start_ost, end_ost, video_state, 
                dest_spk=video_spk_input, output_dir=output_dir, timestamp_list=timestamp_list, add_sub=False)
            return clip_video_file, None, message, clip_srt
        if audio_state is not None:
            (sr, res_audio), message, clip_srt = audio_clipper.clip(
                dest_text, start_ost, end_ost, audio_state, 
                dest_spk=video_spk_input, output_dir=output_dir, timestamp_list=timestamp_list, add_sub=False)
            return None, (sr, res_audio), message, clip_srt
     """
    def parse_grouped_timestamps(LLM_res):
        """解析LLM返回的分组时间戳"""
        groups = []
        current_group = []
        for line in LLM_res.split('
'):
            if line.startswith('组'):
                if current_group:
                    groups.append(current_group)
                    current_group = []
            elif line.strip() and '[' in line and ']' in line:
                current_group.append(line)
        if current_group:
            groups.append(current_group)
        return groups

    def merge_group_timestamps(group):
        """合并组内所有片段的时间范围"""
        # 将组内所有文本拼接成一个字符串
        group_text = '
'.join(group)
        # 直接调用extract_timestamps函数解析时间戳
        return extract_timestamps(group_text)
        
    def AI_clip(LLM_res, dest_text, video_spk_input, start_ost, end_ost, video_state, audio_state, output_dir, clip_count):
        # 解析分组
        groups = parse_grouped_timestamps(LLM_res)
        groups = groups[:int(clip_count)] if clip_count else groups

        # 创建输出目录
        output_dir = output_dir.strip()
        if not len(output_dir):
            output_dir = os.path.abspath(os.path.dirname(__file__))
        llm_video_dir = os.path.join(output_dir, "llmvideo")
        os.makedirs(llm_video_dir, exist_ok=True)

        results = []
        for group_idx, group in enumerate(groups, 1):
            print("group_idx = ", group_idx)
            # 合并组内时间戳
            timestamps = merge_group_timestamps(group)
            if not timestamps:
                continue
                
            # 提取组内文本内容
            group_text = " ".join([item.split(']')[-1].strip() for item in group])
            
            # 计算组内时间范围(毫秒转换为秒)
            group_start = min([ts[0] for ts in timestamps]) / 1000
            group_end = max([ts[1] for ts in timestamps]) / 1000

            print("group_text = ", group_text)
            #print("group_start = ", group_start)
            #print("group_end = ", group_end)
            #print("video_state = ", video_state)
            #print("video_spk_input = ", video_spk_input)
            #print("start_ost = ", start_ost)
            #print("timestamps = ", timestamps)

            if video_state is not None:
                clip_video_file, message, clip_srt = audio_clipper.video_clip(
                    group_text,
                    group_start + (start_ost/1000),  # 转换为秒
                    group_end + (end_ost/1000),      # 转换为秒
                    video_state,
                    dest_spk=video_spk_input,
                    output_dir=llm_video_dir,
                    timestamp_list=timestamps,
                    add_sub=False)
                
                if clip_video_file:
                    # 修改为带时间的文件名
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    #new_path = os.path.join(llm_video_dir, f"group_{group_idx}.mp4")
                    new_path = os.path.join(llm_video_dir, f"{timestamp}_group_{group_idx}.mp4")
                    os.rename(clip_video_file, new_path)
                    results.append((new_path, None, message, clip_srt))               
        return results[0] if results else (None, None, "No clips generated", None)
    def AI_clip_subti(LLM_res, dest_text, video_spk_input, start_ost, end_ost, video_state, audio_state, output_dir):
        timestamp_list = extract_timestamps(LLM_res)
        output_dir = output_dir.strip()
        if not len(output_dir):
            output_dir = None
        else:
            output_dir = os.path.abspath(output_dir)
        if video_state is not None:
            clip_video_file, message, clip_srt = audio_clipper.video_clip(
                dest_text, start_ost, end_ost, video_state, 
                dest_spk=video_spk_input, output_dir=output_dir, timestamp_list=timestamp_list, add_sub=True)
            return clip_video_file, None, message, clip_srt
        if audio_state is not None:
            (sr, res_audio), message, clip_srt = audio_clipper.clip(
                dest_text, start_ost, end_ost, audio_state, 
                dest_spk=video_spk_input, output_dir= output_dir, timestamp_list=timestamp_list, add_sub=True)
            return None, (sr, res_audio), message, clip_srt
    
    # gradio interface
    theme = gr.Theme.load("funclip/utils/theme.json")
    with gr.Blocks(theme=theme) as funclip_service