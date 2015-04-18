class CreateYtVideos < ActiveRecord::Migration
  def change
    create_table :yt_videos do |t|
      t.integer :user_id
      t.string :url

      t.timestamps
    end
  end
end
