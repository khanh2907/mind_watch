class RateController < ApplicationController
  before_filter :authenticate_user!
  
  def facebook_photos
  	@photos = current_user.get_photos
  	@photosString = @photos.to_s
  end

  def youtube
  	@youtube_video = current_user.yt_videos.new

    @previous_videos = current_user.yt_videos.where.not(eeg_data: nil)
  end

  def youtube_video_create
    url = params['yt_video']['url']
    yt = current_user.yt_videos.create(url: url)
    redirect_to yt_watch_and_record_path(yt)
  end

  def youtube_watch_and_record
    @youtube_video = YtVideo.find(params[:id])
  end

  def youtube_video_update
    @youtube_video = YtVideo.find(params[:id])
    @youtube_video.eeg_data = params['yt_video']['eeg_data']
    @youtube_video.save!
    redirect_to yt_replay_path(@youtube_video)
  end

  def youtube_replay
    @youtube_video = YtVideo.find(params[:id])
  end
end