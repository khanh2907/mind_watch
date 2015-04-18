Rails.application.routes.draw do
  root to: 'visitors#index'
  devise_for :users, :controllers => { :omniauth_callbacks => "users/omniauth_callbacks" }
  devise_scope :user do
  	get 'sign_out', :to => 'devise/sessions#destroy', :as => :destroy_user_session
	end
  resources :users

  get 'fbphotos', :to => 'rate#facebook_photos', :as => :rate_facebook_photos
  get 'youtube', :to => 'rate#youtube', :as => :rate_youtube

  post 'yt_videos', :to => 'rate#youtube_video_create', :as => :yt_videos
  patch 'yt_video/:id', :to => 'rate#youtube_video_update', :as => :yt_video

  get 'youtube/:id', :to => 'rate#youtube_watch_and_record', :as => :yt_watch_and_record
  get 'youtube/replay/:id', :to => 'rate#youtube_replay', :as => :yt_replay
end
