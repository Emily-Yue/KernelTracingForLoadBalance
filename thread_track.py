#!/usr/bin/python
#
# urandomread  Example of instrumenting a kernel tracepoint.
#              For Linux, uses BCC, BPF. Embedded C.
#
# REQUIRES: Linux 4.7+ (BPF_PROG_TYPE_TRACEPOINT support).
#
# Test by running this, then in another shell, run:
#     dd if=/dev/urandom of=/dev/null bs=1k count=5
#
# Copyright 2016 Netflix, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")

from __future__ import print_function
from bcc import BPF
from time import sleep

# load BPF program


prog="""

#include <uapi/linux/ptrace.h>
#include <uapi/linux/bpf_perf_event.h>
#include <linux/sched.h>

BPF_PERF_OUTPUT(events);

struct data_t {
    int type; // type of event
    u64 ts;
    int cpu;
    unsigned int len;
    char comm[TASK_COMM_LEN];
    u32 pid_all;
    
    // only for migrate task 
    int src_cpu;
    
    // only for switch and wait
    u32 pid; 
    
    
};

struct cfs_rq_partial {
    struct load_weight load;
#if LINUX_VERSION_CODE < KERNEL_VERSION(5, 7, 0)
    RUNNABLE_WEIGHT_FIELD
#endif
    unsigned int nr_running, h_nr_running;
};

// thread start

TRACEPOINT_PROBE(sched, sched_wakeup) {
    // args is from /sys/kernel/debug/tracing/events/random/urandom_read/format
    int cpu = bpf_get_smp_processor_id();
    // u64 tid = bpf_get_current_pid_tgid();
    u64 pid_tgid = bpf_get_current_pid_tgid();
    u32 pid = pid_tgid >> 32;
    unsigned int len = 0;
    struct task_struct *task = NULL;
    struct cfs_rq_partial *my_q = NULL;
    struct cfs_rq_partial *my_q2 = NULL;
    task = (struct task_struct *)bpf_get_current_task();
    my_q = (struct cfs_rq_partial *)task->se.cfs_rq;
    my_q2 = (struct cfs_rq_partial *)task->se.my_q;
    // len = my_q->nr_running + my_q2->nr_running;
    len = my_q->h_nr_running;
    
    struct data_t data = {};
    
    data.type = 1;
    data.ts = bpf_ktime_get_ns();
    data.cpu = cpu;
    data.len = len;
    data.pid_all = pid;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
      
    events.perf_submit(args, &data, sizeof(data));
  
   
    // bpf_trace_printk("target_cpu %d, Wakeup on CPU %d with %d\\n", args->target_cpu, cpu, len);
    return 0;
};


TRACEPOINT_PROBE(sched, sched_wakeup_new) {
    // args is from /sys/kernel/debug/tracing/events/random/urandom_read/format
    int cpu = bpf_get_smp_processor_id();
    // u64 tid = bpf_get_current_pid_tgid();
    u64 pid_tgid = bpf_get_current_pid_tgid();
    u32 pid = pid_tgid >> 32;
    unsigned int len = 0;
    struct task_struct *task = NULL;
    struct cfs_rq_partial *my_q = NULL;
    struct cfs_rq_partial *my_q2 = NULL;
    task = (struct task_struct *)bpf_get_current_task();
    my_q = (struct cfs_rq_partial *)task->se.cfs_rq;
    my_q2 = (struct cfs_rq_partial *)task->se.my_q;
    // len = my_q->nr_running + my_q2->nr_running;
    len = my_q->h_nr_running;
    
    struct data_t data = {};
    
    data.type = 2;
    data.ts = bpf_ktime_get_ns();
    data.cpu = cpu;
    data.len = len;
    data.pid_all = pid;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    
    events.perf_submit(args, &data, sizeof(data));
    
    
    // bpf_trace_printk("target_cpu %d, New Wakeup on CPU %d with %d\\n", args->target_cpu, cpu, len);
    return 0;
};

TRACEPOINT_PROBE(sched, sched_wake_idle_without_ipi) {
    // args is from /sys/kernel/debug/tracing/events/random/urandom_read/format
    int cpu = bpf_get_smp_processor_id();
    // u64 tid = bpf_get_current_pid_tgid();
    u64 pid_tgid = bpf_get_current_pid_tgid();
    u32 pid = pid_tgid >> 32;
    unsigned int len = 0;
    struct task_struct *task = NULL;
    struct cfs_rq_partial *my_q = NULL;
    struct cfs_rq_partial *my_q2 = NULL;
    task = (struct task_struct *)bpf_get_current_task();
    my_q = (struct cfs_rq_partial *)task->se.cfs_rq;
    my_q2 = (struct cfs_rq_partial *)task->se.my_q;
    // len = my_q->nr_running + my_q2->nr_running;
    len = my_q->h_nr_running;
    
    struct data_t data = {};
    
    data.type = 3;
    data.ts = bpf_ktime_get_ns();
    data.cpu = cpu;
    data.len = len;
    data.pid_all = pid;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    
    events.perf_submit(args, &data, sizeof(data));
    
    
    // bpf_trace_printk("cpu: %d, Wakeup on idle CPU %d with %d\\n", args->cpu, cpu, len);
    return 0;
};


// changing tasks

TRACEPOINT_PROBE(sched, sched_migrate_task) {
    // args is from /sys/kernel/debug/tracing/events/random/urandom_read/format
    int cpu = bpf_get_smp_processor_id();
    // u64 tid = bpf_get_current_pid_tgid();
    u64 pid_tgid = bpf_get_current_pid_tgid();
    u32 pid = pid_tgid >> 32;
    unsigned int len = 0;
    struct task_struct *task = NULL;
    struct cfs_rq_partial *my_q = NULL;
    struct cfs_rq_partial *my_q2 = NULL;
    task = (struct task_struct *)bpf_get_current_task();
    my_q = (struct cfs_rq_partial *)task->se.cfs_rq;
    my_q2 = (struct cfs_rq_partial *)task->se.my_q;
    // len = my_q->nr_running + my_q2->nr_running;
    len = my_q->nr_running;
    
    struct data_t data = {};
    
    data.type = 4;
    data.ts = bpf_ktime_get_ns();
    data.cpu = args->dest_cpu;
    data.src_cpu = args->orig_cpu;
    data.len = len;
    data.pid_all = pid;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    
    events.perf_submit(args, &data, sizeof(data));
    
    bpf_trace_printk("CPU %d --> CPU %d with %d\\n", args->orig_cpu, args->dest_cpu, len);
    return 0;
};


// thread end



TRACEPOINT_PROBE(sched, sched_switch) {
    // args is from /sys/kernel/debug/tracing/events/random/urandom_read/format
    int cpu = bpf_get_smp_processor_id();
    // u64 tid = bpf_get_current_pid_tgid();
    u64 pid_tgid = bpf_get_current_pid_tgid();
    u32 pid = pid_tgid >> 32;
    u32 tid = (u32)pid_tgid;
    unsigned int len = 0;
    
    struct task_struct *task = NULL;
    struct cfs_rq_partial *my_q = NULL;
    struct cfs_rq_partial *my_q2 = NULL;
    
    task = (struct task_struct *)bpf_get_current_task();
    my_q = (struct cfs_rq_partial *)task->se.cfs_rq;
    my_q2 = (struct cfs_rq_partial *)task->se.my_q;
    
    len = my_q->nr_running + my_q2->nr_running;
    // len = my_q->h_nr_running;
    // prev_pid is current thread, so has not switched yet
    
    struct data_t data = {};
    
    data.type = 5;
    data.ts = bpf_ktime_get_ns();
    data.cpu = cpu;
    data.pid = args->next_pid;
    data.len = len;
    data.pid_all = pid;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    
    events.perf_submit(args, &data, sizeof(data));
    
    
    bpf_trace_printk("switch to thread %d on CPU %d with %d\\n", args->next_pid, cpu, len);
    
    return 0;
};


TRACEPOINT_PROBE(sched, sched_wait_task) {
    // args is from /sys/kernel/debug/tracing/events/random/urandom_read/format
    int cpu = bpf_get_smp_processor_id();
    unsigned int len = 0;
    u64 pid_tgid = bpf_get_current_pid_tgid();
    u32 pid = pid_tgid >> 32;
    
    struct task_struct *task = NULL;
    struct cfs_rq_partial *my_q = NULL;
    struct cfs_rq_partial *my_q2 = NULL;
    
    task = (struct task_struct *)bpf_get_current_task();
    my_q = (struct cfs_rq_partial *)task->se.cfs_rq;
    my_q2 = (struct cfs_rq_partial *)task->se.my_q;
    
    // len = my_q->nr_running + my_q2->nr_running;
    len = my_q->h_nr_running;
    
    struct data_t data = {};
    
    data.type = 6;
    data.ts = bpf_ktime_get_ns();
    data.cpu = cpu;
    data.pid = args->pid;
    data.len = len;
    data.pid_all = pid;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    
    events.perf_submit(args, &data, sizeof(data));
    
    bpf_trace_printk("thread %d wait on CPU %d with %d\\n", args->pid, cpu, len);
    
    return 0;
};


/*
TRACEPOINT_PROBE(sched, sched_process_exit) {
    // args is from /sys/kernel/debug/tracing/events/random/urandom_read/format
    int cpu = bpf_get_smp_processor_id();
    u64 tid = bpf_get_current_pid_tgid();
    unsigned int len = 0;
    struct task_struct *task = NULL;
    struct cfs_rq_partial *my_q = NULL;
    task = (struct task_struct *)bpf_get_current_task();
    my_q = (struct cfs_rq_partial *)task->se.cfs_rq;
    len = my_q->nr_running;	
    
    bpf_trace_printk("Exit CPU %d with %d\\n", cpu, len - 1);
    return 0;
};
*/

int hello(struct pt_regs *ctx) {
    int cpu =  bpf_get_smp_processor_id();
    u64 now = bpf_ktime_get_ns();

    bpf_trace_printk("Load Balancing on %d\\n", cpu);
    return 0;

}

"""
    
b = BPF(text=prog)
# b.attach_kprobe(event="load_balance", fn_name="hello")
# b.attach_kprobe(event="__schedule", fn_name="track_move_begin")
# b.attach_kretprobe(event="__schedule", fn_name="track_move_end")


def print_event(cpu, data, size):
    event = b["events"].event(data)
    type_event = event.type
    ts = event.ts
    cpu_ = event.cpu
    len_rq = event.len
    task = event.comm
    pid_all = event.pid_all
    
    if type_event == 1:
        msg = ("Wakeup on CPU %d with %d" % (cpu_, len_rq))
    elif type_event == 2:
        msg = ("New Wakeup on CPU %d with %d" % (cpu_, len_rq))
    elif type_event == 3:
        msg = ("Wakeup on idle CPU %d with %d" % (cpu_, len_rq))
    elif type_event == 4:
        src_cpu = event.src_cpu
        msg = ("CPU %d --> CPU %d with %d" % (src_cpu, cpu_, len_rq))
    elif type_event == 5:
        pid = event.pid
        msg = ("switch to thread %d on CPU %d with %d" % (pid, cpu_, len_rq))
    else:
        pid = event.pid
        msg = ("thread %d wait on CPU %d with %d" % (pid, cpu_, len_rq))
    
    print("%-18.9f %-16s %-6d %s" % (ts, task, pid_all, msg))

b["events"].open_perf_buffer(print_event)



# header
print("%-18s %-16s %-6s %s" % ("TIME(ns)", "COMM", "PID", "MESSAGE"))
duration = 1
# format output
while 1:
    try:
        sleep(duration)
        
    except KeyboardInterrupt:
        # as cleanup can take many seconds, trap Ctrl-C:
        signal.signal(signal.SIGINT, signal_ignore)
    
    b.perf_buffer_poll()
        
    # try:
        # (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    # except ValueError:
        # continue
    # print("%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
    
    exit()

    
    