import objaverse
import multiprocessing
import random

uids = objaverse.load_uids()
processes = multiprocessing.cpu_count()
random_object_uids = random.sample(uids, 5)

print("finished loading uids")



print()
print()
print(random_object_uids)

objects = objaverse.load_objects(
    uids=random_object_uids,
    download_processes=processes
)
print("finished loading objects")



objects = objaverse.load_objects(uids=random_object_uids)


