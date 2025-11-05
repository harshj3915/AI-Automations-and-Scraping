class PhoneCall < ApplicationRecord
  # Validations
  validates :phone_number, presence: true
  
  # Status values: 'pending', 'calling', 'completed', 'failed', 'busy', 'no-answer'
  validates :status, inclusion: { in: %w[pending calling completed failed busy no-answer] }
  
  # Scopes for easy querying
  scope :pending, -> { where(status: 'pending') }
  scope :completed, -> { where(status: 'completed') }
  scope :failed, -> { where(status: 'failed') }
  scope :recent, -> { order(created_at: :desc) }
  
  # Class methods for statistics
  def self.total_calls
    count
  end
  
  def self.successful_calls
    where(status: 'completed').count
  end
  
  def self.failed_calls
    where(status: ['failed', 'busy', 'no-answer']).count
  end
  
  def self.pending_calls
    where(status: 'pending').count
  end
end
