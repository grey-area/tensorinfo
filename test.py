import numpy as np
import torch
from tensorinfo import tensorinfo


class MyClass(torch.nn.Module):
    def __init__(self):
        super().__init__()

        self.x = torch.zeros(3)
        y = torch.tensor(3).cuda()
        self.register_buffer('z', torch.randn(2, 3, 5))
        self.register_parameter('w', torch.nn.Parameter(torch.tensor(5.)))

    def forward(self):
        temporary_tensor = torch.zeros(5)
        tensorinfo()


if __name__ == '__main__':
    tensor_in_local_scope = torch.tensor([True, False])
    tensorinfo(breakpoint=True)

    c = MyClass()
    c()