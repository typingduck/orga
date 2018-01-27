"""
  A simple model with three kinds of employees;
    10x managers, 1x everything and 10x workers (the red, green, blue
    classes below).

  Income can only be generated at the leaves by the WORK_RATE of the worker
  and nodes with reportees pass the income up (in the model below the middle
  nodes have an impact 0-1 so do not generate wealth themselves).

  While income generation is dictated by the node class, feedback
  performace is universally the same.

  As Red are good managers and Blue are good workers we would expect the
  system to evolve to have a red middle layer and blue leaves.
"""

import logging
import random

log = logging.getLogger(__name__)


class Employee(object):
    """Base class for our employees.

    Peformance is measured by two attibutes:
    if the employee has reportees          : WORK_RATE
    if the employee does not have reportees: MGMT_RATE * reportee.tribute
    """
    COLOR     = None
    WORK_RATE = None
    MGMT_RATE = None

    def __init__(self, name):
        self.name = name
        self.tribute = 0
        self.perf = 1

    def do_work(self, reportees):
        if reportees:
            reportees_work = sum(n.tribute for n in reportees)
            self.tribute = self.MGMT_RATE * reportees_work
        else:
            self.tribute = self.WORK_RATE

    def feedback(self, reportees):
        if reportees:
            peer_tributes = [n.tribute for n in reportees]
            total = sum(peer_tributes)
            for reportee in reportees:
                # direct relationship between tribute and performance
                reportee.perf = performance_review(
                    reportee, peer_tributes, self.perf)

    def color(self):
        return self.COLOR

    def alpha(self):
        return 1

    def __str__(self):
        return '<{}({})>'.format(self.name, self.COLOR)


def performance_review(reportee, peers, manager_perf):
    """Decides based on performance to replace the node or not.

    Relative to performance of peers the employee is replaced or not,
    but with a cutoff low level that the manager knows all peers are not
    performing well.

    Performance calculation also includes a factor or the performance of all
    nodes higher up.
    """
    perf = (0.9 + 0.1 * manager_perf) * (reportee.tribute) / max(peers)
    if random.random() > perf:
        replacement = generate_employee(reportee.name)
        # TODO: currently the graph cannot be modified during each iteration
        # so have to change class like this. Next version will have modifiable
        # graphs.
        reportee.__class__ = replacement.__class__
    #log.debug('{} perf: {:.2f} trib: {:.2f}'.format(reportee, perf, reportee.tribute))
    return perf


class Ceo(Employee):
    """Does not really have an effect, just a placeholder for head of graph."""
    COLOR     = 'gray'
    WORK_RATE = 0.0
    MGMT_RATE = 1


class Red(Employee):
    """Higher than normal management rate."""
    COLOR     = 'r'
    WORK_RATE = 0.1
    MGMT_RATE = 1


class Gre(Employee):
    """Average everything."""
    COLOR     = 'g'
    WORK_RATE =  0.1
    MGMT_RATE =  0.1


class Blu(Employee):
    """Higher than normal work rate"""
    COLOR     = 'b'
    WORK_RATE = 1.0
    MGMT_RATE = 0.1


def generate_employee(nid):
    """Convenience function for the orga engine to generate random samples."""
    if nid == 'a0':
        return Ceo('CEO')
    else:
        return random.choice([Red, Gre, Blu])(nid)

