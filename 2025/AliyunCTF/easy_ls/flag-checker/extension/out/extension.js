"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode_1 = require("vscode");
const node_1 = require("vscode-languageclient/node");
const install_1 = require("./install");
let extensionContext;
let client;
let channel;
async function activate(context) {
    channel = vscode_1.window.createOutputChannel('Flag Language Server');
    channel.appendLine(`flag Language Server initializing ...`);
    extensionContext = context;
    await startClient();
    await didChangeConfigHandler();
    context.subscriptions.push(vscode_1.workspace.onDidChangeConfiguration(didChangeConfigHandler), vscode_1.commands.registerCommand('flag.restartLanguageServer', async function () {
        await client.stop();
        client.outputChannel.dispose();
        await startClient();
        await didChangeConfigHandler();
    }));
}
exports.activate = activate;
function deactivate() {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
exports.deactivate = deactivate;
async function startClient() {
    const args = ['--log-level', vscode_1.workspace.getConfiguration('flag').get('languageServer.logLevel')];
    const binPath = await (0, install_1.install)(extensionContext, channel, 'languageServer');
    if (!binPath) {
        return;
    }
    const executable = {
        command: binPath,
        args: args,
        options: {
            env: process.env,
        },
    };
    channel.appendLine(`flag Language Server will start: '${executable.command} ${executable.args.join(' ')}'`);
    const serverOptions = {
        run: executable,
        debug: executable,
    };
    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'flag' }],
    };
    client = new node_1.LanguageClient('Flag-LS', 'Flag Language Server', serverOptions, clientOptions);
    client.start();
}
async function didChangeConfigHandler() {
    const workspaceConfig = vscode_1.workspace.getConfiguration('flag');
    client.sendNotification(node_1.DidChangeConfigurationNotification.type, {
        settings: {
            log_level: workspaceConfig.get('languageServer.logLevel')
        },
    });
}
//# sourceMappingURL=extension.js.map