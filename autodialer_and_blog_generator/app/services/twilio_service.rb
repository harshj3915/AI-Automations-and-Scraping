class TwilioService
  def initialize
    @account_sid = ENV['TWILIO_ACCOUNT_SID']
    @auth_token = ENV['TWILIO_AUTH_TOKEN']
    @from_number = ENV['TWILIO_PHONE_NUMBER']
    @client = Twilio::REST::Client.new(@account_sid, @auth_token) if @account_sid && @auth_token
  end
  
  # Make a call to a phone number
  def make_call(to_number, message = nil)
    return { error: 'Twilio credentials not configured' } unless @client
    
    begin
      # Generate TwiML inline for the call (no need for public URL)
      twiml = generate_twiml(message)
      
      call = @client.calls.create(
        from: @from_number,
        to: to_number,
        twiml: twiml,  # Using inline TwiML instead of URL
        # status_callback can be omitted for testing since localhost isn't accessible
      )
      
      {
        success: true,
        call_sid: call.sid,
        status: call.status,
        to: call.to,
        from: call.from
      }
    rescue Twilio::REST::RestError => e
      {
        success: false,
        error: e.message,
        error_code: e.code
      }
    rescue => e
      {
        success: false,
        error: e.message
      }
    end
  end
  
  # Make multiple calls
  def make_bulk_calls(phone_numbers, message = nil)
    results = []
    
    phone_numbers.each do |number|
      result = make_call(number, message)
      results << {
        phone_number: number,
        result: result
      }
      
      # Small delay between calls to avoid rate limiting
      sleep(0.5)
    end
    
    results
  end
  
  # Get call status
  def get_call_status(call_sid)
    return { error: 'Twilio credentials not configured' } unless @client
    
    begin
      call = @client.calls(call_sid).fetch
      {
        success: true,
        status: call.status,
        duration: call.duration,
        start_time: call.start_time,
        end_time: call.end_time
      }
    rescue => e
      {
        success: false,
        error: e.message
      }
    end
  end
  
  # Generate TwiML for AI voice
  def generate_twiml(message = nil)
    message ||= "Hello! This is an automated call from the Autodialer application. Thank you for your time."
    
    # Escape XML special characters
    message = message.to_s.gsub('&', '&amp;').gsub('<', '&lt;').gsub('>', '&gt;')
    
    # Using AWS Polly neural voice for better quality
    <<~TWIML
      <?xml version="1.0" encoding="UTF-8"?>
      <Response>
        <Say voice="Polly.Joanna-Neural">
          #{message}
        </Say>
        <Pause length="1"/>
        <Say voice="Polly.Joanna-Neural">
          Goodbye!
        </Say>
      </Response>
    TWIML
  end
end
