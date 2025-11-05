# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[8.1].define(version: 2025_11_05_000002) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "pg_catalog.plpgsql"

  create_table "blog_posts", force: :cascade do |t|
    t.string "author", default: "AI Assistant"
    t.text "content", null: false
    t.datetime "created_at", null: false
    t.boolean "published", default: true
    t.string "slug"
    t.string "title", null: false
    t.datetime "updated_at", null: false
    t.index ["created_at"], name: "index_blog_posts_on_created_at"
    t.index ["published"], name: "index_blog_posts_on_published"
    t.index ["slug"], name: "index_blog_posts_on_slug", unique: true
  end

  create_table "phone_calls", force: :cascade do |t|
    t.string "call_sid"
    t.datetime "created_at", null: false
    t.integer "duration"
    t.text "error_message"
    t.text "notes"
    t.string "phone_number", null: false
    t.string "status", default: "pending"
    t.datetime "updated_at", null: false
    t.index ["call_sid"], name: "index_phone_calls_on_call_sid"
    t.index ["created_at"], name: "index_phone_calls_on_created_at"
    t.index ["status"], name: "index_phone_calls_on_status"
  end
end
