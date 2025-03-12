import datetime

from stargazer.core.config import YamlConfig
from stargazer.monitor.cmp.driver import CMPDriver
from stargazer.monitor.utils import convert_to_influxdb

from sanic import Blueprint
from sanic.log import logger
from sanic import response

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
async def metrics(request):

    resource_id = request.args.get("resource_id")
    username = request.args.get("username")
    password = request.args.get("password")
    host = request.args.get("host")
    minutes = request.args.get("minutes", 5)
    if not resource_id:
        return response.json({"error": "resource_id are required"}, status=400)
    config = get_config("vmware", resource_id)

    driver = CMPDriver(
        username or config["username"],
        password or config["password"],
        "vmware",
        host= host or config["host"],
    )

    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(minutes=minutes)
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M") + ":00"
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M") + ":00"

    data = driver.get_weops_monitor_data(
        resourceId=resource_id,
        StartTime=start_time_str,
        EndTime=end_time_str,
        Period=300,
        Metrics=[],
        context={"resources": [{"bk_obj_id": "vmware_vm"}]}
    )
    influxdb_data = convert_to_influxdb(data)
    logger.info("Metrics data generated....")

    return response.raw(influxdb_data, content_type='text/plain; version=0.0.4; charset=utf-8')
