class CreatePhoneCalls < ActiveRecord::Migration[8.1]
  def change
    create_table :phone_calls do |t|
      t.string :phone_number, null: false
      t.string :status, default: 'pending'
      t.integer :duration
      t.string :call_sid
      t.text :error_message
      t.text :notes

      t.timestamps
    end
    
    add_index :phone_calls, :status
    add_index :phone_calls, :call_sid
    add_index :phone_calls, :created_at
  end
end
