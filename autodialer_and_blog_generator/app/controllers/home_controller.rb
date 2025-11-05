class HomeController < ApplicationController
  def index
    @recent_calls = PhoneCall.recent.limit(5) rescue []
    @recent_posts = BlogPost.published.recent.limit(5) rescue []
    @stats = {
      total_calls: (PhoneCall.total_calls rescue 0),
      successful_calls: (PhoneCall.successful_calls rescue 0),
      total_posts: (BlogPost.count rescue 0)
    }
  end
end
