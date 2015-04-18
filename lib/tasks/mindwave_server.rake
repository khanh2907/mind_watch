require 'em-websocket'
require 'json'
begin
  namespace :mindwave_server do
    task :start => :environment do
      EM.run {
        @channel = EM::Channel.new
        EM::WebSocket.run(:host => "0.0.0.0", :port => 8080) do |ws|
          ws.onopen { |handshake|
            puts "WebSocket connection open"

            sid = @channel.subscribe { |msg| ws.send msg }

            ws.onclose { 
            @channel.unsubscribe(sid)
            puts "Connection closed" 
          }

          ws.onmessage { |msg|
            puts "Recieved message: #{msg}"
            @channel.push "#{msg}"
          }
          }

          
        end
      }
    end
  end
end


