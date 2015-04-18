class RateController < ApplicationController
  before_filter :authenticate_user!
  

  def facebook_photos
  	@photos = current_user.get_photos
  	@photosString = @photos.to_s
  end
end