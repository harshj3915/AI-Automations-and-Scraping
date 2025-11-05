class CreateBlogPosts < ActiveRecord::Migration[8.1]
  def change
    create_table :blog_posts do |t|
      t.string :title, null: false
      t.text :content, null: false
      t.string :author, default: 'AI Assistant'
      t.boolean :published, default: true
      t.string :slug

      t.timestamps
    end
    
    add_index :blog_posts, :slug, unique: true
    add_index :blog_posts, :published
    add_index :blog_posts, :created_at
  end
end
