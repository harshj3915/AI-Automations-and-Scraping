class BlogPostsController < ApplicationController
  before_action :set_blog_post, only: [:show, :edit, :update, :destroy]
  
  # GET /blog
  def index
    @blog_posts = BlogPost.published.recent rescue []
  end
  
  # GET /blog/:id
  def show
  end
  
  # GET /blog/new
  def new
    @blog_post = BlogPost.new
  end
  
  # GET /blog/:id/edit
  def edit
  end
  
  # POST /blog
  def create
    @blog_post = BlogPost.new(blog_post_params)
    
    if @blog_post.save
      redirect_to blog_post_path(@blog_post), notice: 'Blog post was successfully created.'
    else
      render :new
    end
  end
  
  # PATCH/PUT /blog/:id
  def update
    if @blog_post.update(blog_post_params)
      redirect_to blog_post_path(@blog_post), notice: 'Blog post was successfully updated.'
    else
      render :edit
    end
  end
  
  # DELETE /blog/:id
  def destroy
    @blog_post.destroy
    redirect_to blog_posts_path, notice: 'Blog post was successfully deleted.'
  end
  
  # GET /blog/generate
  def generate_form
  end
  
  # POST /blog/generate
  def generate
    titles_input = params[:titles]
    
    if titles_input.blank?
      redirect_to generate_form_blog_posts_path, alert: 'Please provide at least one title'
      return
    end
    
    # Parse titles (format: "Title | Optional details")
    titles_with_details = titles_input.split("\n").map do |line|
      parts = line.split('|').map(&:strip)
      {
        title: parts[0],
        details: parts[1]
      }
    end.reject { |item| item[:title].blank? }
    
    ai_service = AiService.new
    results = ai_service.generate_multiple_posts(titles_with_details)
    
    successful = 0
    failed = 0
    
    results.each do |result|
      if result[:result][:success]
        BlogPost.create(
          title: result[:title],
          content: result[:result][:content],
          slug: result[:title].parameterize
        )
        successful += 1
      else
        failed += 1
      end
    end
    
    redirect_to blog_posts_path, notice: "Generated #{successful} blog posts successfully. #{failed} failed."
  end
  
  private
  
  def set_blog_post
    @blog_post = BlogPost.find(params[:id])
  end
  
  def blog_post_params
    params.require(:blog_post).permit(:title, :content, :author, :published)
  end
end
