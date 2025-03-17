def convert_to_influxdb(data):
    """数据格式转换"""
    influxdb_data = []

    # 遍历所有 resource_id
    for resource_id, metrics in data["data"].items():
        for metric_name, metric_data in metrics.items():

            # 判断 metric_data 是否包含 'dims' 这个 key
            if isinstance(metric_data, dict) and "dims" in metric_data and "values" in metric_data:
                # 说明这个指标是 **有维度的**
                dims = metric_data['dims']  # 维度列表
                values = metric_data['values']  # 时间序列数据

                # 构建维度的 tag 字符串
                tag_str = f"resource_id={resource_id}"
                for dim_key, dim_value in dims:
                    tag_str += f",{dim_key}={dim_value}"

                # 遍历时间序列数据，构造 InfluxDB 行协议
                for timestamp, value in values:
                    influxdb_line = f"{metric_name},{tag_str} value={value} {timestamp}"
                    influxdb_data.append(influxdb_line)

            elif isinstance(metric_data, list):
                # 说明这个指标是 **无维度的**
                for timestamp, value in metric_data:
                    influxdb_line = f"{metric_name},resource_id={resource_id} value={value} {timestamp}"
                    influxdb_data.append(influxdb_line)

    return influxdb_data


def convert_to_prometheus(data):
    """数据格式转换为 Prometheus"""
    prometheus_data = []
    help_type_map = {}  # 存储每个指标的 HELP 和 TYPE 避免重复

    # 遍历所有 resource_id
    for resource_id, metrics in data.items():
        for metric_name, metric_data in metrics.items():
            # 确保 HELP 和 TYPE 只定义一次
            if metric_name not in help_type_map:
                prometheus_data.append(f"# HELP {metric_name} Auto-generated help for {metric_name}")
                prometheus_data.append(f"# TYPE {metric_name} gauge")  # 默认使用 gauge
                help_type_map[metric_name] = True

            if isinstance(metric_data, dict) and "dims" in metric_data and "values" in metric_data:
                # **有维度的指标**
                dims = metric_data['dims']  # 维度列表
                values = metric_data['values']  # 时间序列数据

                # 构建 Prometheus 标签字符串
                label_str = f'resource_id="{resource_id}"'
                for dim_key, dim_value in dims:
                    label_str += f', {dim_key}="{dim_value}"'

                # 遍历时间序列数据，构造 Prometheus 格式
                for timestamp, value in values:
                    prometheus_line = f'{metric_name}{{{label_str}}} {value} {timestamp}'
                    prometheus_data.append(prometheus_line)

            elif isinstance(metric_data, list):
                # **无维度的指标**
                for timestamp, value in metric_data:
                    prometheus_line = f'{metric_name}{{resource_id="{resource_id}"}} {value} {timestamp}'
                    prometheus_data.append(prometheus_line)

    return prometheus_data
