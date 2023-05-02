--%%name=MyQA
--%%type=com.fibaro.binarySwitch

function QuickApp:test(a, b)
    self:debug("TEST", a, b)
end

function QuickApp:pong(x,y)
    self:debug("PONG:",x+y)
end

function QuickApp:testrecieve(n)
    self:debug("I:",n)
end

function QuickApp:testcall(id,n)
    for i=1,n do
       fibaro.call(id,"testrecieve",i)
    end

    print("GLOBAL",fibaro.getGlobalVariable('A'))
end

function QuickApp:onInit()

    -- net.HTTPCall():request("http://a.b.c", {
    --     options = {},
    --     success = function(res)
    --     end,
    --     error = function(err)
    --     end
    -- })
    -- self:debug("0")
    -- setInterval(function()
    --     print("Ping")
    --   end,2000  )

    -- fibaro.call(100,"pong",3,4)
end
