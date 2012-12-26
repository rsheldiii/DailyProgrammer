require 'sinatra'
require 'sequel'


DB = Sequel.connect('mysql://root:8Characters!@localhost/sinatra_notes')
notes = DB[:notes]

get '/' do
  ahref = notes.collect {|note| {:name => note[:name],:path => "/note/"+note[:name]+"/"} }
  erb :index, :locals => {:notes => ahref}
end

get '/note/:name/' do |name|
    notes.filter(:name => name).first[:text]
end