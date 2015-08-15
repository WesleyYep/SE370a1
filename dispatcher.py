# A1 for COMPSCI340/SOFTENG370 2015
# Prepared by Robert Sheehan
# Modified by ...

# You are not allowed to use any sleep calls.

from threading import Lock, Event
from process import State, Type

class Dispatcher():
    """The dispatcher."""

    MAX_PROCESSES = 8

    def __init__(self):
        """Construct the dispatcher."""
        # ...
        self.processList = [];
        self.waitingProcessSet = [None, None, None, None, None, None];

    def set_io_sys(self, io_sys):
        """Set the io subsystem."""
        self.io_sys = io_sys

    def add_process(self, process):
        """Add and start the process."""
        # ...
        if process.type == Type.background:
            for p in self.processList[:-1]:
                p.getEvent().clear();
            self.io_sys.allocate_window_to_process(process, len(self.processList));
            self.processList.append(process);
            self.dispatch_next_process();
        else : #Must be interactive
            process.state = State.waiting;
            index = self.allocateWaitingProcess(process);
            self.io_sys.allocate_window_to_process(process, index);
            e = Event();
            process.setEvent(e);
            e.clear();
            process.start();
            
    def allocateWaitingProcess(self, process):
        for i in range(len(self.waitingProcessSet)):
            if (self.waitingProcessSet[i] == None):
                self.waitingProcessSet[i] = process;
                index = i;
                return index;
        return index;

    def dispatch_next_process(self):
        """Dispatch the process at the top of the stack."""
        # ...
        process = self.processList[-1];
        e = Event();
        process.setEvent(e);
        e.set();
        process.start();

    def to_top(self, process):
        """Move the process to the top of the stack."""
        # ...
        if process in self.waitingProcessSet:
            self.waitingProcessSet[self.waitingProcessSet.index(process)] = None;
        elif process in self.processList:
            self.processList.remove(process);
            for i in range(len(self.processList)):
                self.io_sys.move_process(self.processList[i], i)
        self.io_sys.move_process(process, len(self.processList));
        self.processList.append(process);
        for p in self.processList[:-2]:
            p.getEvent().clear();
        for p in self.processList[-2:]:
            p.getEvent().set();

    def pause_system(self):
        """Pause the currently running process.
        As long as the dispatcher doesn't dispatch another process this
        effectively pauses the system.
        """
        # ...
        for p in self.processList[:]:
            p.getEvent().clear();

    def resume_system(self):
        """Resume running the system."""
        # ...
        for p in self.processList[-2:]:
            p.getEvent().set();
            
    def wait_until_finished(self):
        """Hang around until all runnable processes are finished."""
        # ...

    def proc_finished(self, process):
        """Receive notification that "proc" has finished.
        Only called from running processes.
        """
        # ...
        self.processList.remove(process)
        self.io_sys.remove_window_from_process(process)
        self.bubbleUpStack();
            
    def bubbleUpStack(self):
        for i in range(len(self.processList)):
            self.io_sys.move_process(self.processList[i], i)
        if len(self.processList) > 1:
            self.processList[-2].getEvent().set();
        if len(self.processList) > 0:
            self.processList[-1].getEvent().set();
            
    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        # ...
        self.processList.remove(process)
        process.state = State.waiting;
        #print("proc waiting now>????????");
        index = self.allocateWaitingProcess(process);
        self.io_sys.move_process(process, index);
        self.bubbleUpStack();
        
    def bubbleUpStack(self):
        for i in range(len(self.processList)):
            self.io_sys.move_process(self.processList[i], i)
        if len(self.processList) > 1:
            self.processList[-2].getEvent().set();
        if len(self.processList) > 0:
            self.processList[-1].getEvent().set();
        
    def process_with_id(self, id):
        """Return the process with the id."""
        # ...
        for p in self.processList:
            if (id == p.id):
                return p;
        for p in self.waitingProcessSet:
            if (p != None and id == p.id):
                return p;
        return None

