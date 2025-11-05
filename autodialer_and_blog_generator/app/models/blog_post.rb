class BlogPost < ApplicationRecord
  # Validations
  validates :title, presence: true, length: { minimum: 5, maximum: 200 }
  validates :content, presence: true, length: { minimum: 100 }
  validates :author, presence: true
  
  # Scopes
  scope :published, -> { where(published: true) }
  scope :draft, -> { where(published: false) }
  scope :recent, -> { order(created_at: :desc) }
  
  # Set default author
  before_validation :set_default_author, on: :create
  
  private
  
  def set_default_author
    self.author ||= 'AI Assistant'
  end
end
