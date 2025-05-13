local lspconfig = require("lspconfig")
local configs = require("lspconfig.configs")

if not configs.wildwest_ls then
  configs.wildwest_ls = {
    default_config = {
      -- Use TCP connection instead of stdio
      cmd = {"nc", "localhost", "9999"},  -- Connect to running server
      -- 54.221.151.72 7008
      -- cmd = {"nc", "54.221.151.72", "7008"},  -- Connect to running server
      filetypes = { "go" },
      root_dir = function(fname)
        return vim.fn.getcwd()
      end,
      settings = {},
    },
    docs = {
      description = [[
        A Wild West LSP server that wrangles your Go code with a cowboy twist.
        Runs as a TCP server on port 9999.
      ]],
    },
  }
end

-- Setup the LSP with handlers
lspconfig.wildwest_ls.setup {
    on_attach = function(client, bufnr)
        print("Wild West LSP attached to buffer!")
        
        -- Enable completion triggered by <c-x><c-o>
        vim.api.nvim_buf_set_option(bufnr, 'omnifunc', 'v:lua.vim.lsp.omnifunc')
        
        -- Enable completion
        local function buf_set_keymap(...) vim.api.nvim_buf_set_keymap(bufnr, ...) end
        local opts = { noremap=true, silent=true }
        
        -- Mappings
        buf_set_keymap('i', '<C-Space>', '<C-x><C-o>', opts)
    end,
    
    -- Use default capabilities instead of nvim-cmp ones
    capabilities = vim.lsp.protocol.make_client_capabilities(),
    
    handlers = {
        ["window/showMessage"] = function(err, method, params, client_id)
            -- Format message properly for nvim_notify
            local msg_type = params.type  -- 1 = Error, 2 = Warning, 3 = Info, 4 = Log
            local level = "info"
            if msg_type == 1 then
                level = "error"
            elseif msg_type == 2 then
                level = "warn"
            end
            
            vim.schedule(function()
                -- Format multiline messages
                local msg = tostring(params.message):gsub("\n", " | ")
                vim.notify(msg, vim.log.levels[string.upper(level)], {
                    title = "🤠 Wild West LSP",
                    timeout = 5000,
                })
            end)
        end,
    }
}

