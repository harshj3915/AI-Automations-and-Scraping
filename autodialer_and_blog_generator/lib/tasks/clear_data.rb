# Clear all data from phone calls and blog posts
PhoneCall.destroy_all
BlogPost.destroy_all

puts "Cleared #{PhoneCall.count} phone calls"
puts "Cleared #{BlogPost.count} blog posts"
puts "Database cleaned successfully!"
