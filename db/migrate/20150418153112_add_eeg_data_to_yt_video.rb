class AddEegDataToYtVideo < ActiveRecord::Migration
  def change
    add_column :yt_videos, :eeg_data, :text
  end
end
