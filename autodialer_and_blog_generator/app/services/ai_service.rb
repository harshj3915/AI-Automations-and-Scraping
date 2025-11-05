class AiService
  def initialize
    @api_key = ENV['GEMINI_API_KEY']
  end
  
  # Parse natural language command for phone calls
  def parse_call_command(user_input)
    return { error: 'Gemini API key not configured' } unless @api_key
    
    begin
      prompt = <<~PROMPT
        You are a helpful assistant that extracts phone numbers and call instructions from user input.
        If the user wants to make a call, extract the phone number and any message they want to convey.
        Respond ONLY with valid JSON in this format (no markdown, no code blocks):
        {
          "action": "make_call",
          "phone_number": "+1234567890",
          "message": "optional custom message"
        }
        If no phone number is found, respond with:
        {
          "action": "none",
          "error": "No phone number found in the input"
        }
        
        IMPORTANT: The phone number MUST start with + and country code (e.g., +1 for USA, +91 for India).
        
        User input: #{user_input}
      PROMPT
      
      response = HTTParty.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=#{@api_key}",
        headers: { 'Content-Type' => 'application/json' },
        body: {
          contents: [{
            parts: [{ text: prompt }]
          }],
          generationConfig: {
            temperature: 0.3,
            maxOutputTokens: 500
          }
        }.to_json
      )
      
      if response.success?
        content = response.dig('candidates', 0, 'content', 'parts', 0, 'text')
        content = content.gsub(/```json\n|\n```|```/, '').strip
        parsed = JSON.parse(content)
        parsed.symbolize_keys
      else
        { error: response['error']['message'] || 'API request failed' }
      end
    rescue JSON::ParserError => e
      { error: "Failed to parse AI response: #{e.message}" }
    rescue => e
      { error: e.message }
    end
  end
  
  # Generate blog content
  def generate_blog_content(title, details = nil)
    return { error: 'Gemini API key not configured' } unless @api_key
    
    prompt = "You are a professional technical writer specializing in programming topics. Write clear, informative, and engaging articles.\n\n"
    prompt += "Write a comprehensive, professional blog post about: #{title}"
    prompt += "\n\nAdditional details: #{details}" if details.present?
    prompt += "\n\nThe article should be informative, well-structured with headings, and at least 800 words long."
    
    begin
      response = HTTParty.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=#{@api_key}",
        headers: { 'Content-Type' => 'application/json' },
        body: {
          contents: [{
            parts: [{ text: prompt }]
          }],
          generationConfig: {
            temperature: 0.7,
            maxOutputTokens: 8000
          }
        }.to_json
      )
      
      if response.success?
        content = response.dig('candidates', 0, 'content', 'parts', 0, 'text')
        { success: true, content: content }
      else
        { success: false, error: response['error']['message'] || 'API request failed' }
      end
    rescue => e
      { success: false, error: e.message }
    end
  end
  
  # Generate multiple blog posts
  def generate_multiple_posts(titles_with_details)
    results = []
    
    titles_with_details.each do |item|
      title = item[:title]
      details = item[:details]
      
      result = generate_blog_content(title, details)
      results << {
        title: title,
        result: result
      }
      
      sleep(1)
    end
    
    results
  end
end
