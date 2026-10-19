import React from 'react';
import ReactECharts from 'echarts-for-react';
import type { TrendData } from '../types';
import { format } from 'date-fns';

interface HealthChartProps {
  data: TrendData;
  isDark?: boolean;
}

const HealthChart: React.FC<HealthChartProps> = ({ data, isDark = false }) => {
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
      },
    },
    legend: {
      data: ['Health Score', 'Total Smells'],
      bottom: 0,
      textStyle: {
        color: isDark ? '#9ca3af' : '#6b7280',
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: data.data_points.map((dp) => format(new Date(dp.date), 'MMM d')),
      axisLine: {
        lineStyle: {
          color: isDark ? '#4b5563' : '#d1d5db',
        },
      },
      axisLabel: {
        color: isDark ? '#9ca3af' : '#6b7280',
      },
    },
    yAxis: [
      {
        type: 'value',
        name: 'Health Score',
        min: 0,
        max: 100,
        axisLine: {
          lineStyle: {
            color: isDark ? '#4b5563' : '#d1d5db',
          },
        },
        axisLabel: {
          color: isDark ? '#9ca3af' : '#6b7280',
          formatter: '{value}',
        },
        splitLine: {
          lineStyle: {
            color: isDark ? '#374151' : '#e5e7eb',
          },
        },
      },
      {
        type: 'value',
        name: 'Smells',
        axisLine: {
          lineStyle: {
            color: isDark ? '#4b5563' : '#d1d5db',
          },
        },
        axisLabel: {
          color: isDark ? '#9ca3af' : '#6b7280',
        },
        splitLine: {
          show: false,
        },
      },
    ],
    series: [
      {
        name: 'Health Score',
        type: 'line',
        smooth: true,
        data: data.data_points.map((dp) => dp.health_score),
        lineStyle: {
          width: 3,
          color: '#0ea5e9',
        },
        itemStyle: {
          color: '#0ea5e9',
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(14, 165, 233, 0.3)' },
              { offset: 1, color: 'rgba(14, 165, 233, 0)' },
            ],
          },
        },
        markLine: {
          silent: true,
          lineStyle: {
            color: '#ef4444',
            type: 'dashed',
          },
          data: [
            { yAxis: 80, name: 'Good' },
            { yAxis: 60, name: 'Warning' },
          ],
          label: {
            formatter: '{b}',
            color: isDark ? '#9ca3af' : '#6b7280',
          },
        },
      },
      {
        name: 'Total Smells',
        type: 'bar',
        yAxisIndex: 1,
        data: data.data_points.map((dp) => dp.total_smells),
        itemStyle: {
          color: isDark ? '#6b7280' : '#9ca3af',
          borderRadius: [4, 4, 0, 0],
        },
      },
    ],
  };

  return (
    <ReactECharts
      option={option}
      style={{ height: '300px', width: '100%' }}
      opts={{ renderer: 'svg' }}
    />
  );
};

export default HealthChart;