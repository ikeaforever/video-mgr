import { Request, Response } from 'express';

// 代码中会兼容本地 service mock 以及部署站点的静态数据
export default {
    // 支持值为 Object 和 Array
    'GET /api/video': (req: Request, res: Response) => {
      res.send({
        success: true,
        total: 2,
        data: [{
            id:1,
            name: "非洲动物大迁徙",
            category: {
                id: 0,
                name: "默认"
            },
            file_size: 12121212,
            play_info_size: 120100
        },
        {
            id:2,
            name: "动物搞笑视频",
            category: {
                id: 1,
                name: "搞笑"
            },
            file_size: 18271721,
            play_info_size: 23828328
        }
    ],
      });
    }
}