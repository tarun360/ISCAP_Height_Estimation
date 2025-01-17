# you can change cmd.sh depending on what type of queue you are using.
# If you have no queueing system and want to run on a local machine, you
# can change all instances 'queue.pl' to run.pl (but be careful and run
# commands one by one: most recipes will exhaust the memory on your
# machine).  queue.pl works with GridEngine (qsub).  slurm.pl works
# with slurm.  Different queues are configured differently, with different
# queue names and different ways of specifying things like memory;
# to account for these differences you can create and edit the file
# conf/queue.conf to match your queue's configuration.  Search for
# conf/queue.conf in http://kaldi-asr.org/doc/queue.html for more information,
# or search for the string 'default_config' in utils/queue.pl or utils/slurm.pl.

# export train_cmd="/home/tungtest/slurm.pl "
# export cuda_cmd="/home/tungtest/slurm.pl --gpu 1 --nodelist=node08 "
# export cuda_cmd_alt="/home/tungtest/slurm.pl --gpu 1 --nodelist=node06 "
# #export cuda_cmd="/home/tungtest/slurm.pl --gpu 1 "
# export decode_cmd="/home/tungtest/slurm.pl --quiet"
# export cuda_cmd_all="/home/tungtest/slurm.pl --gpu 1 --exclude=node01,node02"
# export cuda_cmd_all_bigGPU="/home/tungtest/slurm.pl --gpu 1 --exclude=node01,node02,node03,node04,node05,node06,node07"
# export cuda_cmd_all_rmNode3="/home/tungtest/slurm.pl --gpu 1 --exclude=node01,node02,node03"
# export cuda_cmd_all_goodGPU="/home/tungtest/slurm.pl --gpu 1 --exclude=node01,node02,node03,node04,node05,node06 "
# export cuda_cmd_all_goodGPU2="/home/tungtest/slurm.pl --gpu 1 --exclude=node01,node02,node03,node04,node05,node06,node07 "


export train_cmd="run.pl --mem 2G"
export cuda_cmd="run.pl --mem 2G --gpu 1"
export decode_cmd="run.pl --mem 4G"
