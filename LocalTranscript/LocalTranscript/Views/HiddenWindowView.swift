import SwiftUI

struct HiddenWindowView: View {
    var body: some View {
        Color.clear
            .frame(width: 1, height: 1)
            .onReceive(NotificationCenter.default.publisher(for: .openSettingsRequest)) { _ in
                Task { @MainActor in
                    // Temporarily show dock icon so Settings can receive focus
                    NSApp.setActivationPolicy(.regular)
                    try? await Task.sleep(for: .milliseconds(100))

                    NSApp.activate(ignoringOtherApps: true)

                    // Open Settings window using NSApp sendAction
                    if #available(macOS 14.0, *) {
                        NSApp.sendAction(Selector(("showSettingsWindow:")), to: nil, from: nil)
                    } else {
                        NSApp.sendAction(Selector(("showPreferencesWindow:")), to: nil, from: nil)
                    }

                    try? await Task.sleep(for: .milliseconds(200))
                    if let window = NSApp.windows.first(where: {
                        $0.identifier?.rawValue == "com.apple.SwiftUI.Settings" ||
                        $0.title.localizedCaseInsensitiveContains("settings")
                    }) {
                        window.makeKeyAndOrderFront(nil)
                        window.orderFrontRegardless()
                    }
                }
            }
            .onReceive(NotificationCenter.default.publisher(for: .settingsWindowClosed)) { _ in
                // Hide dock icon again
                NSApp.setActivationPolicy(.accessory)
            }
    }
}

extension Notification.Name {
    static let openSettingsRequest = Notification.Name("openSettingsRequest")
    static let settingsWindowClosed = Notification.Name("settingsWindowClosed")
}
