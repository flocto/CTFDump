"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.install = void 0;
const vscode_1 = require("vscode");
const fs = require("fs");
const path = require("path");
const ComponentDetails = {
    languageServer: {
        binaryName: 'flag-LS.exe',
        displayName: '',
    },
};
async function install(context, channel, component) {
    const { binaryName, displayName } = ComponentDetails[component];
    let binPath = vscode_1.workspace.getConfiguration('flag').get(`${component}.pathToBinary`);
    binPath = path.join(context.extensionPath, 'bin', binaryName);
    const binPathExists = fs.existsSync(binPath);
    channel.appendLine(`Binary path is ${binPath} (exists: ${binPathExists})`);
    return binPath;
}
exports.install = install;
//# sourceMappingURL=install.js.map