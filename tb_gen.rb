require 'fileutils'

default_image = '/images/default-thumbnail.jpg'
md_files = Dir.glob('_posts/*.md')

md_files.each do |file|
  content = File.read(file)
  # 코드 블록 제거
  content_without_code = content.gsub(/```.*?```/m, '')
  # 이미지 추출
  image_url = content_without_code[/!\[.*?\]\((.*?)\)/, 1] || default_image

  # date 아래에 feature_image 삽입
  new_content = content.sub(/(date:.*?\n)/, "\\1feature_image: #{image_url}\n")
  File.write(file, new_content)
end