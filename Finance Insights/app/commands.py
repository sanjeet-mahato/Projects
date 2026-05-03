import click
from flask import current_app
import redis


def register_commands(app):
    """Register CLI commands for the app"""

    @app.cli.command()
    def cleanup_sessions():
        """Delete expired sessions from Redis"""
        try:
            redis_client = current_app.config['SESSION_REDIS']
            # Redis automatically expires keys, but we can manually clean up
            # Get all session keys (they start with 'session:')
            session_keys = redis_client.keys('session:*')
            cleaned_count = 0

            for key in session_keys:
                # Check if key has TTL (time to live)
                ttl = redis_client.ttl(key)
                if ttl == -2:  # Key doesn't exist
                    continue
                elif ttl == -1:  # Key has no expiration
                    # For non-permanent sessions, we might want to clean them up
                    # But let's be conservative and only clean expired ones
                    continue
                elif ttl == 0:  # Key is expired
                    redis_client.delete(key)
                    cleaned_count += 1

            click.echo(f"✅ Cleaned up {cleaned_count} expired session(s)")
        except Exception as e:
            click.echo(f"❌ Error cleaning up sessions: {str(e)}")

    @app.cli.command()
    def cleanup_all_sessions():
        """Delete ALL sessions from Redis (use with caution!)"""
        try:
            redis_client = current_app.config['SESSION_REDIS']
            session_keys = redis_client.keys('session:*')
            if session_keys:
                deleted_count = redis_client.delete(*session_keys)
                click.echo(f"⚠️  Deleted {deleted_count} session(s)")
            else:
                click.echo("No sessions found")
        except Exception as e:
            click.echo(f"❌ Error cleaning up sessions: {str(e)}")

    @app.cli.command()
    def check_sessions():
        """Check current transaction data in Redis"""
        try:
            redis_client = current_app.config['SESSION_REDIS']
            # Look for transaction data keys
            transaction_keys = redis_client.keys('transaction_data:*')

            if not transaction_keys:
                click.echo("No transaction data found in Redis")
                return

            click.echo(f"\n📊 Transaction Data in Redis: {len(transaction_keys)}\n")

            for key in transaction_keys:
                key_str = key.decode('utf-8') if isinstance(key, bytes) else key
                ttl = redis_client.ttl(key)

                if ttl == -1:
                    ttl_str = "No expiration"
                elif ttl == -2:
                    ttl_str = "Expired (should be cleaned up)"
                else:
                    ttl_str = f"Expires in {ttl} seconds"

                click.echo(f"  Key: {key_str}")
                click.echo(f"  TTL: {ttl_str}")

                # Try to get data size and transaction count
                try:
                    data = redis_client.get(key)
                    if data:
                        import json
                        parsed = json.loads(data)
                        size_kb = len(data) / 1024
                        click.echo(f"  Size: {size_kb:.2f} KB")
                        click.echo(f"  Transactions: {parsed.get('total_transactions', 'unknown')}")
                        click.echo(f"  Timestamp: {parsed.get('timestamp', 'unknown')}")
                except:
                    pass

                click.echo("")

        except Exception as e:
            click.echo(f"❌ Error checking transaction data: {str(e)}")

    @app.cli.command()
    def redis_info():
        """Show Redis connection information"""
        try:
            redis_client = current_app.config['SESSION_REDIS']
            info = redis_client.info()

            click.echo("🔴 Redis Connection Info:")
            click.echo(f"  Host: {redis_client.connection_pool.connection_kwargs.get('host', 'unknown')}")
            click.echo(f"  Port: {redis_client.connection_pool.connection_kwargs.get('port', 'unknown')}")
            click.echo(f"  Database: {redis_client.connection_pool.connection_kwargs.get('db', 'unknown')}")
            click.echo(f"  Connected: {'✅' if redis_client.ping() else '❌'}")
            click.echo(f"  Memory Used: {info.get('used_memory_human', 'unknown')}")
            click.echo(f"  Total Connections: {info.get('total_connections_received', 'unknown')}")

        except Exception as e:
            click.echo(f"❌ Redis connection error: {str(e)}")
