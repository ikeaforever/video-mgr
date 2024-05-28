import { video } from '@/services/ant-design-pro/api';
import type { ProColumns } from '@ant-design/pro-components';
import { PageContainer, ProTable } from '@ant-design/pro-components';
import { FormattedMessage } from '@umijs/max';
import { filesize } from 'filesize';
import React from 'react';


const VideoList: React.FC = () => {
  const columns: ProColumns<API.VideoItem>[] = [
    {
      title: <FormattedMessage defaultMessage="ID" id='id'/>,
      dataIndex: 'id',
      search: false
    },
    {
      title: <FormattedMessage defaultMessage="名称" id='name' />,
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: '分类',
      dataIndex: ['category', 'name'],
      key: 'category',
    },
    {
      title: '源文件',
      dataIndex: 'file_size',
      key: 'file_size',
      render: (dom, entity) => {
        let file_size =entity.file_size?entity.file_size:0;
        return <>{filesize(file_size)}</>;
      },
    },
    {
      title: '解码文件',
      dataIndex: 'play_info_size',
      key: 'play_info_size',
      render: (dom, entity) => {
        let file_size =entity.play_info_size?entity.play_info_size:0;
        return <>{filesize(file_size)}</>;
      },
    },
  ];
  return (
    <PageContainer>
      <ProTable<API.VideoItem, API.PageParams>
        // params 是需要自带的参数
        // 这个参数优先级更高，会覆盖查询表单的参数
        request={video}
        columns={columns}
      />
    </PageContainer>
  );
};
export default VideoList;
