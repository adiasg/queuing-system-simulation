import random
import matplotlib.pyplot as plt

# lambda_exp = mean rate of arrival
# mu = mean rate of service

class Customer:
  def __init__(self, arrival_time, service_start_time, service_time):
    self.arrival_time = arrival_time
    self.service_start_time = service_start_time
    self.service_time = service_time
    self.service_end_time = self.service_start_time + self.service_time
    self.wait_time = self.service_end_time - self.arrival_time
  
def exp(lambda_exp):
  return random.expovariate(lambda_exp)
  
def simulate(mu, lambda_exp, end_time):
  t = 0
  Customers = []
  arrival_time = 0
  while t < end_time:
    arrival_time = arrival_time + exp(lambda_exp)
    if (len(Customers)==0):
      service_start_time = arrival_time
    else:
      service_start_time = max(arrival_time, Customers[-1].service_end_time)
    service_time = exp(mu)
    #if(service_start_time+service_time<=end_time):
    Customers.append(Customer(arrival_time, service_start_time, service_time))
    t = arrival_time
  
  wait_times = []
  service_times = []
  total_served_customers = 0
  total_unserved_customers = 0
  
  for c in Customers:
    if(c.service_end_time <= end_time):
      wait_times.append(c.wait_time)
      service_times.append(c.service_time)
      total_served_customers = total_served_customers + 1
    elif(c.service_start_time < end_time):
      service_times.append(c.service_time)
      total_unserved_customers = total_unserved_customers + 1
    elif(c.arrival_time < end_time):
      wait_times.append(end_time - c.arrival_time)
      total_unserved_customers = total_unserved_customers + 1
       
  total_wait_time = sum(wait_times)
  mean_wait_time = total_wait_time/len(wait_times)
  total_service_time = sum(service_times)
  mean_service_time = total_service_time/len(service_times)
  server_idle_time = end_time - total_service_time
  
  
  mean_total_time = (total_wait_time + total_service_time) / (total_served_customers + total_unserved_customers)
  
  arrival_times = [c.arrival_time for c in Customers]
  service_end_times = [c.service_end_time for c in Customers]
  
  t = 0
  step = end_time/100.0
  customers_in_range = []
  time_range_start = []
  i,j,prev_count = 0,0,0
  while(t<end_time):
    time_range_start.append(t)
    arrivals, departures = 0, 0
    while(i<len(arrival_times) and arrival_times[i]<t+step):
      arrivals = arrivals + 1
      i = i + 1
    while(j<len(service_end_times) and service_end_times[j]<t+step):
      departures = departures + 1
      j = j + 1
    #print("time_range: ", time_range_start[-1])
    #print("arrivals: ", arrivals)
    #print("departures: ", departures)
    count = arrivals-departures+prev_count
    customers_in_range.append(count)
    #print("customers_in_range: ", customers_in_range[-1])
    prev_count = count
    t = t + step
  
  plt.plot(time_range_start, customers_in_range)
  plt.xlabel('Time')
  plt.ylabel('No. of Customers')
  plt.show()
  
  print "Number of served customers: ", total_served_customers
  print "Number of unfinished customers: ", total_unserved_customers
  print "Mean Service Time: ", mean_service_time
  print "Mean Wait Time: ", mean_wait_time
  print "Mean Total Time: ", mean_total_time
  print "Total Service Time: ", total_service_time
  print "Server Idle Time: ", server_idle_time
  print "Server Idle Ratio: ", server_idle_time/end_time
  
print("Enter parameters:")
lambda_exp = int(input("Mean rate of arrival\nlambda: "))
mu = int(input("Mean rate of service\nmu: "))
end_time = int(input("simulation time: "))
simulate(mu, lambda_exp, end_time)
#simulate(4, 5, 20000)
