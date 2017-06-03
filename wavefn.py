import math
import operator


class WaveFn:

	def __init__(self, k_val, x_unit, x_bound, type="even"):
		self.k = k_val
		self.unit = x_unit
		self.x_bound = x_bound
		self.x_val = self._init_x()
		self.y_val = self._init_y()
		self.type = type

		assert len(self.x_val) == len(self.y_val), "len x_val:%d, len y_val:%d" % (len(self.x_val), len(self.y_val))
				

	def _init_y(self):
		count = math.floor(self.x_bound/self.unit)
		lst = [0 for _ in range(2*count + 1)]
		return lst

	def _init_x(self):
		lst = list()
		total_count = math.floor(self.x_bound/self.unit)*2 + 1
		i = 0
		tmp = -1*self.x_bound
		while i < total_count:
			lst.append(tmp)
			tmp += self.unit
			i += 1
		return lst



	def _compute_data(self):
		second_deriv_lst = self._init_y()

		mid = len(self.y_val)//2
		if self.type == "even":
			self.y_val[mid] = 0.5
			self.y_val[mid+1] = 0.499999
			self.y_val[mid-1] = 0.499999
		elif self.type == "odd":
			self.y_val[mid] = 0
			self.y_val[mid+1] = -0.000001
			self.y_val[mid-1] = 0.000001

		# first calcuate the positive range
		i = mid+1
		while i < len(self.y_val)-1:
			prev = i
			prev_val = self.x_val[i]
			i += 1
			second_deriv_lst[prev] = (math.pow(prev_val,2) - self.k)*self.y_val[prev]
			self.y_val[i] = 2*self.y_val[prev] - self.y_val[prev-1] + second_deriv_lst[prev]*math.pow(self.unit, 2)

		# then calculate the negative range
		i = mid-1
		while i > 0:
			prev = i
			prev_val = self.x_val[i]
			i -= 1
			second_deriv_lst[prev] = (math.pow(prev_val,2) - self.k)*self.y_val[prev]
			self.y_val[i] = 2*self.y_val[prev] - self.y_val[prev+1] + second_deriv_lst[prev]*math.pow(self.unit, 2)
	

	def get_data(self):
		self._compute_data()
		return self.y_val


# if __name__ == "__main__":
# 	test = WaveFn(0.5, 0.1, 1)
# 	test.get_range()

	# Note, initial condition can closely related to the resolution/stepsize


