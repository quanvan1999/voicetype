import Foundation
import AsyncQueue

/// Actor-based FIFO queue for sequential transcription processing
///
/// Ensures transcription segments are processed in order, even when
/// multiple segments are queued rapidly during continuous dictation.
///
/// Usage:
/// ```swift
/// let queue = TranscriptionQueue()
///
/// // Enqueue a transcription operation
/// let result = try await queue.enqueue {
///     // Transcription work here
///     return "transcribed text"
/// }
/// ```
actor TranscriptionQueue {
    /// Maximum queue depth before rejecting new segments
    static let maxDepth = 5

    private let fifoQueue = FIFOQueue()
    private var _pendingCount: Int = 0

    /// Number of segments currently pending transcription
    var pendingCount: Int {
        _pendingCount
    }

    /// Whether the queue is empty
    var isEmpty: Bool {
        _pendingCount == 0
    }

    /// Whether the queue is at capacity
    var isFull: Bool {
        _pendingCount >= Self.maxDepth
    }

    /// Enqueue a transcription operation for FIFO processing
    ///
    /// Operations are guaranteed to execute in the order they were enqueued.
    /// Each operation runs to completion before the next begins.
    ///
    /// - Parameter operation: Async closure that performs transcription and returns result
    /// - Returns: The transcription result from the operation
    /// - Throws: TranscriptionQueueError.queueFull if at capacity, or any error from the operation
    func enqueue(_ operation: @Sendable @escaping () async throws -> String) async throws -> String {
        // Check queue depth
        guard !isFull else {
            throw TranscriptionQueueError.queueFull(currentDepth: _pendingCount)
        }

        // Increment pending count
        _pendingCount += 1

        defer { _pendingCount -= 1 }

        // Execute on FIFO queue to ensure ordering
        return try await fifoQueue.enqueueAndWait {
            try await operation()
        }
    }

    /// Enqueue a transcription operation that returns an optional result
    ///
    /// Convenience method for operations that may not produce output (e.g., empty audio).
    ///
    /// - Parameter operation: Async closure that performs transcription
    /// - Returns: The transcription result, or nil if operation returned nil
    func enqueueOptional(_ operation: @Sendable @escaping () async throws -> String?) async throws -> String? {
        guard !isFull else {
            throw TranscriptionQueueError.queueFull(currentDepth: _pendingCount)
        }

        _pendingCount += 1

        defer { _pendingCount -= 1 }

        return try await fifoQueue.enqueueAndWait {
            try await operation()
        }
    }
}

/// Errors from the transcription queue
enum TranscriptionQueueError: LocalizedError {
    case queueFull(currentDepth: Int)

    var errorDescription: String? {
        switch self {
        case .queueFull(let depth):
            return "Transcription queue is full (\(depth) segments pending). Please wait for processing to complete."
        }
    }
}
