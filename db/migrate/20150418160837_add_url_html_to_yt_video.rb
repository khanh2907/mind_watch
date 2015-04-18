class AddUrlHtmlToYtVideo < ActiveRecord::Migration
  def change
    add_column :yt_videos, :url_html, :text
  end
end
