import { PageContainer } from '@ant-design/pro-components';
import React from 'react';
import { Table } from "antd";
import {filesize} from "filesize";

const dataSource = [
  {
    id: '1',
    name: '动物迁移大冒险',
    category: {
      id: 1,
      name:'默认'
    },
    file_size: 121212,
    play_info_size: 231212,
  },
  {
    id: '2',
    name: '动物搞笑视频',
    category: {
      id: 1,
      name:'默认'
    },
    file_size: 908821212,
    play_info_size: 123312231212,
  },
];

const columns = [
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
  },
  {
    title: '名称',
    dataIndex: 'name',
    key: 'name',
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
    render: (size: string) => {
      return <>{filesize(size)}</>
    }
  },
  {
    title: '解码文件',
    dataIndex: 'play_info_size',
    key: 'play_info_size',
    render: (size: string) => {
      return <>{filesize(size)}</>
    }
  },
];

const VideoList: React.FC = () => {
  return (
    <PageContainer>
      <Table dataSource={dataSource} columns={columns} />;
    </PageContainer>
  )
}
export default VideoList;