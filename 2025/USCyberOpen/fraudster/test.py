import scapy.all as scapy
import sys
from collections import defaultdict
import statistics

def analyze_packet_timing(pcap_file):
    packets = scapy.rdpcap(pcap_file)
    
    http_responses = []
    
    # Extract HTTP responses with timestamps
    for packet in packets:
        if (packet.haslayer(scapy.TCP) and 
            packet.haslayer(scapy.Raw) and
            packet[scapy.TCP].sport == 8002):
            
            try:
                http_data = packet[scapy.Raw].load.decode('utf-8', errors='ignore')
                if http_data.startswith('HTTP/'):
                    response_info = {
                        'timestamp': float(packet.time),
                        'packet_num': len(http_responses) + 1,
                        'src_ip': packet[scapy.IP].src,
                        'dst_ip': packet[scapy.IP].dst,
                        'tcp_seq': packet[scapy.TCP].seq,
                        'tcp_ack': packet[scapy.TCP].ack,
                        'tcp_options': packet[scapy.TCP].options
                    }
                    http_responses.append(response_info)
            except:
                continue
    
    if len(http_responses) < 2:
        print("Need at least 2 HTTP responses for timing analysis")
        return
    
    print(f"Found {len(http_responses)} HTTP responses for timing analysis\n")
    
    # Calculate time differences between consecutive packets
    time_diffs = []
    for i in range(1, len(http_responses)):
        diff = http_responses[i]['timestamp'] - http_responses[i-1]['timestamp']
        time_diffs.append(diff)
        print(f"Response {i} to {i+1}: {diff:.6f} seconds")
    
    print(f"\n=== Timing Statistics ===")
    print(f"Total responses: {len(http_responses)}")
    print(f"Time span: {http_responses[-1]['timestamp'] - http_responses[0]['timestamp']:.6f} seconds")
    print(f"Average interval: {statistics.mean(time_diffs):.6f} seconds")
    print(f"Median interval: {statistics.median(time_diffs):.6f} seconds")
    print(f"Min interval: {min(time_diffs):.6f} seconds")
    print(f"Max interval: {max(time_diffs):.6f} seconds")
    print(f"Standard deviation: {statistics.stdev(time_diffs):.6f} seconds")
    
    # Analyze TCP timestamp options for more precise timing
    print(f"\n=== TCP Timestamp Analysis ===")
    tcp_timestamps = []
    for resp in http_responses:
        ts_val = None
        for opt in resp['tcp_options']:
            if opt[0] == 'Timestamp':
                ts_val = opt[1][0]  # TSval (sender timestamp)
                break
        tcp_timestamps.append(ts_val)
        print(f"Response {resp['packet_num']}: TCP TSval = {ts_val}")
    
    # Calculate TCP timestamp differences (these are in system ticks, not seconds)
    if all(ts is not None for ts in tcp_timestamps):
        tcp_diffs = []
        for i in range(1, len(tcp_timestamps)):
            diff = tcp_timestamps[i] - tcp_timestamps[i-1]
            tcp_diffs.append(diff)
            print(f"TCP timestamp diff {i} to {i+1}: {diff} ticks")
        
        print(f"\nTCP Timestamp Statistics:")
        print(f"Average tick diff: {statistics.mean(tcp_diffs):.2f}")
        print(f"Tick diff std dev: {statistics.stdev(tcp_diffs):.2f}")
    
    # Look for suspicious patterns
    print(f"\n=== Suspicious Pattern Detection ===")
    
    # 1. Unusually fast responses (< 1ms)
    fast_responses = [i for i, diff in enumerate(time_diffs) if diff < 0.001]
    if fast_responses:
        print(f"⚠️  Suspiciously fast responses (< 1ms): {len(fast_responses)} found")
        for idx in fast_responses:
            print(f"   Response {idx+1} to {idx+2}: {time_diffs[idx]*1000:.3f}ms")
    
    # 2. Perfect timing intervals (suggesting automation)
    rounded_diffs = [round(diff, 3) for diff in time_diffs]
    timing_counts = defaultdict(int)
    for diff in rounded_diffs:
        timing_counts[diff] += 1
    
    repeated_timings = {k: v for k, v in timing_counts.items() if v > 1}
    if repeated_timings:
        print(f"⚠️  Repeated timing intervals (possible automation):")
        for timing, count in sorted(repeated_timings.items()):
            print(f"   {timing:.3f}s appears {count} times")
    
    # 3. Outliers (more than 2 standard deviations from mean)
    if len(time_diffs) > 3:
        mean_diff = statistics.mean(time_diffs)
        std_diff = statistics.stdev(time_diffs)
        threshold = 2 * std_diff
        
        outliers = []
        for i, diff in enumerate(time_diffs):
            if abs(diff - mean_diff) > threshold:
                outliers.append((i, diff))
        
        if outliers:
            print(f"⚠️  Timing outliers (>2σ from mean):")
            for idx, diff in outliers:
                print(f"   Response {idx+1} to {idx+2}: {diff:.6f}s (deviation: {abs(diff - mean_diff):.6f}s)")
    
    # 4. Check for burst patterns
    burst_threshold = statistics.mean(time_diffs) / 10  # Much faster than average
    burst_sequences = []
    current_burst = []
    
    for i, diff in enumerate(time_diffs):
        if diff < burst_threshold:
            current_burst.append(i)
        else:
            if len(current_burst) >= 3:  # Burst of 3+ fast responses
                burst_sequences.append(current_burst)
            current_burst = []
    
    if len(current_burst) >= 3:
        burst_sequences.append(current_burst)
    
    if burst_sequences:
        print(f"⚠️  Burst patterns detected:")
        for burst in burst_sequences:
            print(f"   Burst from response {burst[0]+1} to {burst[-1]+2} ({len(burst)+1} responses)")
    
    # 5. Analysis by source characteristics
    print(f"\n=== Source Analysis ===")
    
    # Group by TCP timestamp characteristics to identify different systems
    timestamp_patterns = defaultdict(list)
    for i, resp in enumerate(http_responses):
        ts_opts = str([opt for opt in resp['tcp_options'] if opt[0] == 'Timestamp'])
        timestamp_patterns[ts_opts].append(i)
    
    if len(timestamp_patterns) > 1:
        print(f"⚠️  Multiple TCP timestamp patterns detected (possible different systems):")
        for pattern, indices in timestamp_patterns.items():
            print(f"   Pattern: {pattern[:100]}...")
            print(f"   Responses: {indices[:10]}{'...' if len(indices) > 10 else ''} ({len(indices)} total)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python timing_analysis.py <pcap_file>")
        sys.exit(1)
    
    analyze_packet_timing(sys.argv[1])