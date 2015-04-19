class CreateBlinks < ActiveRecord::Migration
  def change
    create_table :blinks do |t|
      t.integer :user_id
      t.integer :score

      t.timestamps
    end
  end
end
