import datetime
import pytz

local_time = datetime.datetime.now() - datetime.timedelta(hours=30)
print(local_time)
print(datetime.datetime.now(datetime.timezone.utc))
belarus_time = pytz.timezone("Europe/Minsk")
amsterdam_time = pytz.timezone("Europe/Amsterdam")
belarus_local_time_aware_object = belarus_time.localize(local_time)
print(belarus_time)
print(belarus_local_time_aware_object)
amsterdam_time_from_belarus_time = belarus_local_time_aware_object.astimezone(amsterdam_time)
print(amsterdam_time_from_belarus_time)
