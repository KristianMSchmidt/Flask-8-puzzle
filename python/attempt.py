from heapq import heappush, heappop
import Puzzle
p=Puzzle.Puzzle(3,3)
h = []
heappush(h, (5, 'write code'))
heappush(h, (7, 'release product'))
heappush(h, (1, 'write spec'))
heappush(h, (p.manhattan_dist(), p))
print(h)

#heappush(frontier, (self.manhattan_dist(), self))
