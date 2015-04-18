class YtVideo < ActiveRecord::Base
	belongs_to :user

	auto_html_for :url do
    youtube(:width => 1100, :height => 500, :autoplay => true, :enablejsapi => 1, :version => 3, :playerapiid => 'ytplayer')
  end
end
