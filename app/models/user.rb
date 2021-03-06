class User < ActiveRecord::Base
  enum role: [:user, :vip, :admin]
  after_initialize :set_default_role, :if => :new_record?

  has_many :yt_videos
  has_many :blinks

  def set_default_role
    self.role ||= :user
  end

  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable and :omniauthable
  devise :omniauthable, :omniauth_providers => [:facebook]

   def self.new_with_session(params, session)
    super.tap do |user|
      if data = session["devise.facebook_data"] && session["devise.facebook_data"]["extra"]["raw_info"]
        user.email = data["email"] if user.email.blank?
      end
    end
  end

  def self.from_omniauth(auth)
	  this_user = where(provider: auth.provider, uid: auth.uid).first_or_create do |user|
	    user.email = auth.info.email || 'test@example.com'
	    user.name = auth.info.name 
	  end
    this_user.fb_token = auth.credentials.token
    this_user.save
    return this_user
	end

  def fb_picture
    facebook = Koala::Facebook::API.new(fb_token)
    facebook.get_object("me?fields=picture.type(large) ")['picture']['data']['url']
  end

  def get_friends
    facebook = Koala::Facebook::API.new(fb_token)
    facebook.get_connections("me", "friends")
  end

  def get_photos
    facebook = Koala::Facebook::API.new(fb_token)
    facebook.get_connections("me", "photos?limit=3&offset=#{rand(0..300)}").map{|i| i['images'][1]['source']}.shuffle
  end
end
