from concurrent.futures import ThreadPoolExecutor
from alibabacloud_vod20170321.client import Client as vod20170321Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_vod20170321 import models as vod_20170321_models
from alibabacloud_tea_util import models as util_models

from backend import DBSession, Task, Category, Video

PAGE_SIZE = 100


# 分类id和分类名字对应表
cate_map = {
    0: "未分类",
}

class AliYunVodClient(object):
    def __init__(self, access_key, access_secret, endpoint):
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @param endpoint:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            access_key_id=access_key,
            access_key_secret=access_secret,
            endpoint=endpoint
        )
        self.client = vod20170321Client(config)
    
    def get_categories(self):
        """
        get cates of aliyun videos
        """
        get_categories_request = vod_20170321_models.GetCategoriesRequest()
        get_categories_request.page_size = PAGE_SIZE
        runtime = util_models.RuntimeOptions()

        cate_id_list = []
        resp = self.client.get_categories_with_options(get_categories_request, runtime)

        cate_list = resp.body.sub_categories.category
        for cates in cate_list:
            cate_map[cates.cate_id] = cates.cate_name
            cate_id_list.append(cates.cate_id)
        total_count = resp.body.sub_total
        if total_count is None:
            total_count = 0
        if total_count > PAGE_SIZE:
            for i in range(2, total_count // PAGE_SIZE + 2):
                get_categories_request.page_no = i
                new_resp = self.client.get_categories_with_options(get_categories_request, runtime)
                cate_list = new_resp.body.sub_categories.category
                # 获取所有的分类id，不包括没有分类的（cate_id为0是未分类）
                for cates in cate_list:
                    cate_map[cates.cate_id] = cates.cate_name
                    cate_id_list.append(cates.cate_id)

        # query all categories, if cate_id not in, add it to database, else update it
        for cate_id in cate_id_list:
            cate = DBSession.query(Category).filter(Category.id == cate_id).first()
            if cate is None:
                cate = Category(id=cate_id, name=cate_map[cate_id])
                DBSession.add(cate)
                DBSession.commit()
            else:
                cate.name = cate_map[cate_id]
                DBSession.commit()

    def search_media(self):
        """
        原视频大小和列表
        """
        # find all the category in db
        cate_id_list = []
        for cate in DBSession.query(Category).all():
            cate_id_list.append(cate.id)
        
        category_videos = {}
        for cate_id in cate_id_list:
            source_file_size = 0
            vid_list = []
            # for cate_id in tqdm(cate_id_list, desc="搜索源视频中"):
            search_media_request = vod_20170321_models.SearchMediaRequest(
                fields='Size,CateId',
                page_size=PAGE_SIZE,
                match="CateId = " + str(cate_id),
            )
            runtime = util_models.RuntimeOptions()

            resp = self.client.search_media_with_options(search_media_request, runtime)
            token = resp.body.scroll_token
            media_list = resp.body.media_list
            total_count = resp.body.total
            if total_count > PAGE_SIZE:
                for i in range(2, total_count // PAGE_SIZE + 2):
                    search_media_request.page_no = i
                    search_media_request.scroll_token = token
                    new_resp = self.client.search_media_with_options(search_media_request, runtime)
                    token = new_resp.body.scroll_token
                    new_media_list = new_resp.body.media_list
                    media_list += new_media_list

            for media in media_list:
                # 计算源文件大小
                media_video_size = media.video.size if media.video.size else 0
                source_file_size += media_video_size / 1073741824
                # 收集源文件对应的转码后的视频id
                vid_list.append(media.video.video_id)
        
            category_videos[cate_id] = {
                "source_file_size": source_file_size,
                "transcode_file_size": 0,
                "vid_list": vid_list
            }
        # iter category_videos, if video not in video table,add it to db or update it
        for cate_id in category_videos:
            cate_info = category_videos[cate_id]
            cate_videos_size = cate_info["source_file_size"]
            cate_transcode_videos_size = cate_info["transcode_file_size"]
            cate_vid_list = cate_info["vid_list"]
            cate_videos = DBSession.query(Video).filter(Video.video_id.in_(cate_vid_list)).all()
            for video in cate_videos:
                video.cate_id = cate_id
                video.source_file_size = cate_videos_size
                video.transcode_file_size = cate_transcode_videos_size
                DBSession.commit()
            
    def process_video(self, vid):
        get_play_info_request = vod_20170321_models.GetPlayInfoRequest()
        get_play_info_request.video_id = vid
        runtime = util_models.RuntimeOptions()

        try:
            resp = self.client.get_play_info_with_options(get_play_info_request, runtime)
            play_info_list = resp.body.play_info_list.play_info
            for play_info in play_info_list:
                # 累加转码后的视频size
                play_info_size = play_info.size if play_info.size else 0
                
                # update video play_info_size bt video_id
                video = DBSession.query(Video).filter(Video.video_id == vid).first()
                video.play_info_size = play_info_size
                DBSession.commit()
                
        except Exception as error:
            print(error)


def calculate_size(access_key, access_secret, endpoint) -> None:
    
    try:
        client = AliYunVodClient(access_key, access_secret, endpoint)

        client.search_media()
        client.get_play_info()

        # get all video from db, use process_video update play_info_size in parallel
        video_list = DBSession.query(Video).all()
        with ThreadPoolExecutor(max_workers=10) as executor:
            for video in video_list:
                executor.submit(client.process_video, video.video_id)

    except Exception as error:
        print(error)


if __name__ == '__main__':

    access_key = ""
    access_secret = ""
    endpoint = f'vod.cn-shenzhen.aliyuncs.com'

    calculate_size(access_key, access_secret, endpoint)
