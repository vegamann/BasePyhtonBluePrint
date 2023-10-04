require 'yaml'

file = YAML.load_file('./docker-compose.yml')
network_names = file['networks'].map{ |network| network[0] }
services = file['services']
services_info = services.keys.map do |key|
  {
    name: key.strip,
    networks: services[key]['networks'].compact
  }
end

network_hash = {}
services_info.each do |service|
  service[:networks].each do |network_name|
    network_hash[network_name] ||= []
    network_hash[network_name] << service[:name]
  end
end

only_five_networks = network_hash.values.count == 5
global_network_exist = network_hash.values.select{ |services_in_network| services_in_network.uniq.count == 4  }.count == 1
concrete_networks = network_hash.values.select{ |services_in_network| services_in_network.uniq.count == 2  }
concrete_networks_exist = concrete_networks.count == 4

all_service_in_only_one_concrete = services_info.all? do |service|
  name = service[:name]
  concrete_networks.select{ |network| network.include?(name) }.count == 1
end


all_conditions_met = global_network_exist && only_five_networks && concrete_networks_exist && all_service_in_only_one_concrete

if !all_conditions_met
  raise 'Bad networks'
else
  puts "OK"
end