from pyzabbix import ZabbixAPI
from datetime import datetime, timedelta
from pprint import pprint
import time

class Parser:
    def get_zapi(self, uri, user, passwd):
        zapi = ZabbixAPI(uri)
        zapi.login(user=user, password=passwd)
        return zapi


    def get_recent_problems(self, uri, user, passwd, days=7):
        zapi = self.get_zapi(uri, user, passwd)
        messages : list[str] = []
        try:
            time_from = int((datetime.now() - timedelta(days=days)).timestamp())

            # Only ACTIVE problems that STARTED within last 7 days.
            # problem.get by default returns unresolved (active) problems.
            problems = zapi.problem.get(
                output=["eventid", "clock", "name", "severity", "objectid"],
                selectTags="extend",
                selectAcknowledges="extend",
                time_from=time_from,
            # no sortfield/sortorder here – not allowed for problem.get in some versions
                severities=[3,4,5],
                limit=200
            )
            # Sort by clock DESC client-side (newest first)
            problems.sort(key=lambda p: int(p["clock"]), reverse=True)
            count = 0 
            for p in problems:
                eventid = p["eventid"]
                trigger_id = p["objectid"]
                clock_human = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(p["clock"])))

                # Trigger info (host + description)
                trig = zapi.trigger.get(
                    output=["description"],
                    selectHosts=["hostid", "name"],
                    triggerids=trigger_id
                )
                if not trig:
                    # Trigger might be deleted/hidden by permissions; skip gracefully
                    hosts, desc = [], "(trigger not accessible)"
                else:
                    trig = trig[0]
                    hosts = [h["name"] for h in trig.get("hosts", [])]
                    desc = trig.get("description", "")

                # Alerts (messages) sent for this event.
                # time_from optional here; eventid is enough. Keep it to trim noise if desired.
                alerts = zapi.alert.get(
                    output=["alertid", "subject", "message", "sendto", "clock", "status", "error", "mediatypeid"],
                    eventids=eventid,
                    time_from=time_from,  # safe to keep; remove if you want all alerts since event start
                    sortfield="clock",    # allowed for alert.get
                    sortorder="ASC"
                )

                # Pretty format alerts
                alerts_pretty = [{
                    "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(a["clock"]))),
                    "to": a.get("sendto"),
                    "status": a.get("status"),  # 1=sent, 0=pending, 2=failed (varies by version)
                    "error": a.get("error", ""),
                    "subject": a.get("subject", ""),
                    "message": a.get("message", "")
                } for a in alerts]
                if len(alerts_pretty):
                    message = str()
                    message +=  f"Host(s): {hosts} \n"
                    message += f"Problem: {desc} \n"
                    message += f"Started : {clock_human}\n"
                    message += "Messages sent by actions:"
                    message += alerts_pretty[0]["message"][:1000]
                    messages.append(message)
            return messages

        finally:
            zapi.user.logout()    
        return messages 




  
