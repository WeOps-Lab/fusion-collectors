import datetime

from core.config import YamlConfig
from monitor.cmp.driver import CMPDriver
from monitor.utils import convert_to_influxdb

from sanic import Blueprint
from sanic.log import logger
from sanic import response

from plugins.vmware_info import VmwareManage

yml_config = YamlConfig(path="./config.yml")

monitor_router = Blueprint("monitor", url_prefix="/monitor")


def get_config(monitor_type: str, monitor_instance: str):

    """
    Get the configuration for the monitor type and instance
    :param monitor_type:
    :param monitor_instance:
    :return: dict
    """
    config = yml_config.get(monitor_type, {}).get(monitor_instance, {})

    return config


@monitor_router.get("/vmware/metrics")
async def vmware_metrics(request):

    username = request.args.get("username")
    password = request.args.get("password")
    host = request.args.get("host")
    minutes = request.args.get("minutes", 5)
    # resource_id = request.args.get("resource_id")
    # if not resource_id:
    #     return response.json({"error": "resource_id are required"}, status=400)
    # config = get_config("vmware", resource_id)

    driver = CMPDriver(
        username,
        password,
        "vmware",
        host= host,
    )

    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(minutes=int(minutes))
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M") + ":00"
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M") + ":00"

    object_map = VmwareManage(params=dict(
        username=username,
        password=password,
        hostname=host,
    )).service()

    metric_list = []
    for object_id, object_list in object_map.items():
        if object_id == "vmware_vc":
            continue
        for object_info in object_list:
            resource_id = object_info["inst_name"]
            data = driver.get_weops_monitor_data(
                resourceId=resource_id,
                StartTime=start_time_str,
                EndTime=end_time_str,
                Period=300,
                Metrics=[],
                context={"resources": [{"bk_obj_id": object_id}]}
            )
            if not data["result"]:
                logger.error(f"resource_id: {resource_id}, message: {data.get('message')}")
                continue
            item = convert_to_influxdb(data)
            metric_list.extend(item)

    influxdb_data = "\n".join(metric_list)
    logger.info("Metrics data generated....")

    return response.raw(influxdb_data, content_type='text/plain; version=0.0.4; charset=utf-8')
