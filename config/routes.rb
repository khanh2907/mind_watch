Rails.application.routes.draw do
  root to: 'visitors#index'
  devise_for :users, :controllers => { :omniauth_callbacks => "users/omniauth_callbacks" }
  devise_scope :user do
  	get 'sign_out', :to => 'devise/sessions#destroy', :as => :destroy_user_session
	end
  resources :users

  get 'fbphotos', :to => 'rate#facebook_photos', :as => :rate_facebook_photos
  get 'youtube', :to => 'rate#youtube', :as => :rate_youtube

  post 'yt_videos', :to => 'rate#youtube_videos', :as => :yt_videos
end
