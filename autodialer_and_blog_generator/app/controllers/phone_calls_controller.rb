class PhoneCallsController < ApplicationController
  skip_before_action :verify_authenticity_token, only: [:twilio_callback, :twiml]
  
  # GET /phone_calls
  def index
    @phone_calls = PhoneCall.order(created_at: :desc).limit(50)
    @stats = {
      total: (PhoneCall.total_calls rescue 0),
      successful: (PhoneCall.successful_calls rescue 0),
      failed: (PhoneCall.failed_calls rescue 0),
      pending: (PhoneCall.pending_calls rescue 0)
    }
  end
  
  # GET /phone_calls/new
  def new
    @phone_call = PhoneCall.new
  end
  
  # POST /phone_calls
  def create
    phone_numbers = extract_phone_numbers
    
    if phone_numbers.empty?
      redirect_to new_phone_call_path, alert: 'No valid phone numbers found'
      return
    end
    
    twilio_service = TwilioService.new
    message = params[:message]
    
    results = twilio_service.make_bulk_calls(phone_numbers, message)
    
    # Save results to database
    results.each do |result|
      phone_call = PhoneCall.create(
        phone_number: result[:phone_number],
        status: result[:result][:success] ? 'calling' : 'failed',
        call_sid: result[:result][:call_sid],
        error_message: result[:result][:error]
      ) rescue nil
    end
    
    successful = results.count { |r| r[:result][:success] }
    failed = results.count { |r| !r[:result][:success] }
    
    redirect_to phone_calls_path, notice: "Calls initiated: #{successful} successful, #{failed} failed"
  end
  
  # POST /phone_calls/ai_command
  def ai_command
    user_input = params[:command]
    
    ai_service = AiService.new
    parsed = ai_service.parse_call_command(user_input)
    
    # Convert string keys to symbols if needed
    parsed = parsed.symbolize_keys if parsed.is_a?(Hash)
    
    if parsed[:error] || parsed[:action] == 'none'
      error_msg = parsed[:error] || 'Could not understand the command'
      # Log the error in database
      PhoneCall.create(
        phone_number: 'N/A',
        status: 'failed',
        error_message: "AI Command Error: #{error_msg}",
        notes: "Failed AI command: #{user_input}"
      )
      redirect_to phone_calls_path, alert: error_msg
      return
    end
    
    phone_number = parsed[:phone_number]
    message = parsed[:message]
    
    # Validate phone number exists
    if phone_number.blank?
      PhoneCall.create(
        phone_number: 'N/A',
        status: 'failed',
        error_message: 'No phone number extracted from AI command',
        notes: "Failed AI command: #{user_input}"
      )
      redirect_to phone_calls_path, alert: 'No phone number found in command'
      return
    end
    
    twilio_service = TwilioService.new
    result = twilio_service.make_call(phone_number, message)
    
    phone_call = PhoneCall.create(
      phone_number: phone_number,
      status: result[:success] ? 'calling' : 'failed',
      call_sid: result[:call_sid],
      error_message: result[:error],
      notes: "Created via AI command: #{user_input}"
    )
    
    if result[:success]
      redirect_to phone_calls_path, notice: "Call initiated to #{phone_number}"
    else
      redirect_to phone_calls_path, alert: "Call failed: #{result[:error]}"
    end
  end
  
  # POST /twilio/callback
  def twilio_callback
    call_sid = params['CallSid']
    status = params['CallStatus']
    duration = params['CallDuration']
    
    phone_call = PhoneCall.find_by(call_sid: call_sid)
    if phone_call
      phone_call.update(
        status: status,
        duration: duration
      )
    end
    
    head :ok
  end
  
  # GET /twiml
  def twiml
    message = params[:message]
    twilio_service = TwilioService.new
    twiml = twilio_service.generate_twiml(message)
    
    render xml: twiml
  end
  
  # POST /phone_calls/:id/refresh_status
  def refresh_status
    phone_call = PhoneCall.find(params[:id])
    
    if phone_call.call_sid.present?
      twilio_service = TwilioService.new
      result = twilio_service.get_call_status(phone_call.call_sid)
      
      if result[:success]
        phone_call.update(
          status: result[:status],
          duration: result[:duration]
        )
        redirect_to phone_calls_path, notice: "Status updated: #{result[:status]}"
      else
        redirect_to phone_calls_path, alert: "Failed to update status: #{result[:error]}"
      end
    else
      redirect_to phone_calls_path, alert: "No call SID available"
    end
  end
  
  # POST /phone_calls/refresh_all
  def refresh_all
    updated = 0
    PhoneCall.where(status: ['calling', 'queued', 'ringing', 'in-progress']).where.not(call_sid: nil).each do |call|
      twilio_service = TwilioService.new
      result = twilio_service.get_call_status(call.call_sid)
      
      if result[:success]
        call.update(
          status: result[:status],
          duration: result[:duration]
        )
        updated += 1
      end
      sleep(0.2) # Small delay to avoid rate limiting
    end
    
    redirect_to phone_calls_path, notice: "Updated #{updated} call(s)"
  end
  
  private
  
  def extract_phone_numbers
    if params[:phone_numbers].present?
      # Extract from textarea (one per line)
      params[:phone_numbers].split(/[\n,;]/).map(&:strip).reject(&:blank?)
    elsif params[:file].present?
      # Extract from uploaded file
      file = params[:file]
      content = file.read
      content.split(/[\n,;]/).map(&:strip).reject(&:blank?)
    else
      []
    end
  end
end
