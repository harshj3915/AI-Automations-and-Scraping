Rails.application.routes.draw do
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Root path
  root "home#index"
  
  # Home page
  get 'home', to: 'home#index'
  
  # Phone calls routes
  resources :phone_calls, only: [:index, :new, :create] do
    collection do
      post 'ai_command'
      post 'refresh_all'
    end
    member do
      post 'refresh_status'
    end
  end
  
  # Twilio webhooks
  post 'twilio/callback', to: 'phone_calls#twilio_callback', as: :twilio_callback
  get 'twiml', to: 'phone_calls#twiml', as: :twiml
  
  # Blog routes
  resources :blog_posts, path: 'blog' do
    collection do
      get 'generate', to: 'blog_posts#generate_form', as: :generate_form
      post 'generate', to: 'blog_posts#generate'
    end
  end

  # Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
  # Can be used by load balancers and uptime monitors to verify that the app is live.
  get "up" => "rails/health#show", as: :rails_health_check
end
